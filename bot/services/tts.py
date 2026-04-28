import asyncio
import io
import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from aiogram.types import BufferedInputFile

from bot.database.models import Vocabulary

logger = logging.getLogger(__name__)


async def generate_arabic_audio(text: str) -> Optional[io.BytesIO]:
    """Generate Arabic TTS audio as MP3 BytesIO. Returns None on failure."""
    def _generate() -> Optional[io.BytesIO]:
        try:
            from gtts import gTTS
            buf = io.BytesIO()
            tts = gTTS(text=text, lang="ar", slow=False)
            tts.write_to_fp(buf)
            buf.seek(0)
            return buf
        except Exception as e:
            logger.error(f"gTTS generation failed for '{text}': {e}")
            return None

    return await asyncio.to_thread(_generate)


async def get_audio_input_file(arabic_word: str, word_id: int) -> Optional[BufferedInputFile]:
    """Generate fresh TTS audio as BufferedInputFile ready to be sent."""
    audio_buf = await generate_arabic_audio(arabic_word)
    if not audio_buf:
        return None
    return BufferedInputFile(audio_buf.read(), filename=f"word_{word_id}.mp3")


async def cache_audio_file_id(session: AsyncSession, word_id: int, file_id: str) -> None:
    """Save Telegram file_id back to vocabulary so we don't regenerate next time."""
    try:
        await session.execute(
            update(Vocabulary)
            .where(Vocabulary.word_id == word_id)
            .values(telegram_audio_file_id=file_id)
        )
    except Exception as e:
        logger.warning(f"Failed to cache audio file_id for word {word_id}: {e}")
