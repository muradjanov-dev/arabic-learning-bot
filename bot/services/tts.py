import asyncio
import io
import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from aiogram.types import BufferedInputFile

from bot.database.models import Vocabulary

logger = logging.getLogger(__name__)

# HamedNeural is optimized for MSA with full i'rab (case endings/tanwin)
ARABIC_VOICE = "ar-SA-HamedNeural"
ARABIC_VOICE_FALLBACK = "ar-SA-ZariyahNeural"


def _prepare_arabic_tts(text: str) -> str:
    """Prepare Arabic text so TTS speaks full case endings (baytun, not bayt).

    Two-step fix for Azure Neural TTS pausal (waqf) pronunciation:
    1. Expand tanwin diacritics to explicit n-letters (ٌ → ُنْ) as a hint.
    2. Append وَ so the target word is never utterance-final — neural TTS only
       drops case endings on the last token; وَ ("wa") becomes that last token
       instead, and all preceding words are read in connected-speech form.
    """
    # Step 1: tanwin → explicit n
    text = text.replace('ٌ', 'ُنْ')
    text = text.replace('ً', 'َنْ')
    text = text.replace('ٍ', 'ِنْ')
    # Step 2: append وَ to prevent pausal form on the last real word
    text = text.strip()
    if not text.endswith('وَ'):
        text += ' وَ'
    return text


def _is_arabic_script(text: str) -> bool:
    return any('؀' <= c <= 'ۿ' for c in text)


async def generate_arabic_audio(text: str) -> Optional[io.BytesIO]:
    """Generate Arabic TTS with full case endings (MSA connected-speech form)."""
    if _is_arabic_script(text):
        text = _prepare_arabic_tts(text)
    import edge_tts
    for voice in (ARABIC_VOICE, ARABIC_VOICE_FALLBACK):
        try:
            # rate="-15%" ensures word-final case endings (tanwin) are clearly audible
            communicate = edge_tts.Communicate(text, voice=voice, rate="-15%")
            buf = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    buf.write(chunk["data"])
            if buf.tell() > 0:
                buf.seek(0)
                return buf
        except Exception as e:
            logger.warning(f"edge-tts '{voice}' failed for '{text}': {e}")

    # Fallback: gTTS (slow=True for clearer pronunciation)
    def _gtts() -> Optional[io.BytesIO]:
        try:
            from gtts import gTTS
            buf = io.BytesIO()
            tts = gTTS(text=text, lang="ar", slow=True)
            tts.write_to_fp(buf)
            buf.seek(0)
            return buf
        except Exception as ex:
            logger.error(f"gTTS also failed for '{text}': {ex}")
            return None

    return await asyncio.to_thread(_gtts)


async def get_audio_input_file(arabic_word: str, word_id: int) -> Optional[BufferedInputFile]:
    audio_buf = await generate_arabic_audio(arabic_word)
    if not audio_buf:
        return None
    return BufferedInputFile(audio_buf.read(), filename=f"word_{word_id}.mp3")


async def cache_audio_file_id(session: AsyncSession, word_id: int, file_id: str) -> None:
    try:
        await session.execute(
            update(Vocabulary)
            .where(Vocabulary.word_id == word_id)
            .values(telegram_audio_file_id=file_id)
        )
    except Exception as e:
        logger.warning(f"Failed to cache audio file_id for word {word_id}: {e}")
