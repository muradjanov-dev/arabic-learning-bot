"""
Gemini AI content generation via REST API (aiohttp — no extra package needed).
Runs ONCE per vocabulary word, cached in DB. Zero latency during lessons.
"""
import asyncio
import json
import logging
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash-lite:generateContent"
)
_REQUEST_DELAY = 4.5  # stay under 15 RPM free tier limit


def _build_prompt(arabic_word: str, uzbek: str, trans: str, level_id: int) -> str:
    if level_id <= 2:
        complexity = "very simple — 2-3 words, use هذا or هي + this word"
    elif level_id <= 4:
        complexity = "simple — 3-5 words, subject + this word"
    elif level_id <= 6:
        complexity = "moderate — 4-6 words, complete simple sentence"
    else:
        complexity = "natural — 5-8 words, meaningful sentence"

    return (
        f"You are an Arabic teacher for Uzbek-speaking beginners.\n\n"
        f"Arabic word: {arabic_word}\n"
        f"Uzbek meaning: {uzbek}\n"
        f"Pronunciation: {trans}\n"
        f"Level {level_id}/10 — sentence complexity: {complexity}\n\n"
        f"Write ONE example Arabic sentence using this exact word.\n"
        f"Rules: Modern Standard Arabic, full diacritics, grammatically correct.\n\n"
        f"Return ONLY valid JSON, no markdown:\n"
        f'{{ "arabic": "الجملة هنا", "uzbek": "O\'zbek tarjimasi" }}'
    )


async def generate_example_sentence(
    arabic_word: str,
    uzbek_translation: str,
    transliteration: str,
    level_id: int,
) -> tuple[Optional[dict], Optional[str]]:
    """Returns (result, error_message). result is None on failure."""
    from bot.config import settings
    if not settings.GEMINI_API_KEY:
        return None, "GEMINI_API_KEY topilmadi"

    payload = {
        "contents": [{"parts": [{"text": _build_prompt(
            arabic_word, uzbek_translation, transliteration or "", level_id
        )}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 200,
        },
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                GEMINI_URL,
                params={"key": settings.GEMINI_API_KEY},
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    err = f"HTTP {resp.status}: {body[:200]}"
                    logger.error(f"Gemini error for '{arabic_word}': {err}")
                    return None, err

                data = await resp.json()
                raw = data["candidates"][0]["content"]["parts"][0]["text"].strip()

                # Strip markdown fences if present
                if "```" in raw:
                    parts = raw.split("```")
                    raw = parts[1].strip()
                    if raw.startswith("json"):
                        raw = raw[4:].strip()

                result = json.loads(raw)
                if "arabic" in result and "uzbek" in result:
                    return {"arabic": result["arabic"].strip(), "uzbek": result["uzbek"].strip()}, None

                return None, f"Noto'g'ri JSON: {raw[:100]}"

    except Exception as e:
        logger.error(f"Gemini request failed for '{arabic_word}': {e}")
        return None, str(e)[:150]


async def bulk_generate_missing(
    session_factory,
    bot,
    admin_chat_id: int,
    level_filter: Optional[int] = None,
) -> None:
    """Find all words with no example sentence, call Gemini, save to DB."""
    from sqlalchemy import select, and_, update
    from bot.database.models import Vocabulary

    async with session_factory() as session:
        q = (
            select(Vocabulary)
            .where(and_(
                Vocabulary.is_active == True,
                Vocabulary.example_sentence_arabic == None,
                Vocabulary.category.notin_(["harf", "harakat"]),
            ))
            .order_by(Vocabulary.level_id, Vocabulary.topic_id)
        )
        if level_filter:
            q = q.where(Vocabulary.level_id == level_filter)
        words = (await session.execute(q)).scalars().all()

    if not words:
        try:
            await bot.send_message(admin_chat_id, "✅ Barcha so'zlarda misol jumlalar mavjud.")
        except Exception:
            pass
        return

    total = len(words)
    eta_min = int(total * _REQUEST_DELAY / 60)
    try:
        status_msg = await bot.send_message(
            admin_chat_id,
            f"⏳ {total} ta so'z uchun jumlalar yaratilmoqda (~{eta_min} daqiqa)..."
        )
        status_id = status_msg.message_id
    except Exception:
        status_id = None

    done = failed = 0
    first_error: Optional[str] = None

    for word in words:
        result, err = await generate_example_sentence(
            word.arabic_word,
            word.uzbek_translation,
            word.transliteration or "",
            word.level_id,
        )
        if result:
            async with session_factory() as session:
                await session.execute(
                    update(Vocabulary)
                    .where(Vocabulary.word_id == word.word_id)
                    .values(
                        example_sentence_arabic=result["arabic"],
                        example_sentence_uzbek=result["uzbek"],
                    )
                )
                await session.commit()
            done += 1
        else:
            if first_error is None and err:
                first_error = err
            failed += 1

        if status_id and (done + failed) % 10 == 0:
            try:
                pct = int((done + failed) / total * 100)
                await bot.edit_message_text(
                    f"⏳ Yaratilmoqda: {done + failed}/{total} ({pct}%)\n✅ {done}  ❌ {failed}",
                    chat_id=admin_chat_id,
                    message_id=status_id,
                )
            except Exception:
                pass

        await asyncio.sleep(_REQUEST_DELAY)

    summary = (
        f"{'✅' if failed == 0 else '⚠️'} Yaratish yakunlandi!\n\n"
        f"✅ Muvaffaqiyatli: {done}\n"
        f"❌ Xatolik: {failed}\n"
        f"Jami: {total}"
    )
    if first_error:
        summary += f"\n\n🔴 Birinchi xato:\n<code>{first_error}</code>"
    try:
        if status_id:
            await bot.edit_message_text(summary, chat_id=admin_chat_id, message_id=status_id, parse_mode="HTML")
        else:
            await bot.send_message(admin_chat_id, summary, parse_mode="HTML")
    except Exception:
        pass
    logger.info(f"Gemini bulk done: {done}/{total}")


async def auto_generate_on_startup(session_factory, bot) -> None:
    from bot.config import settings
    from bot.database.models import Vocabulary
    from sqlalchemy import select, and_, func

    if not settings.GEMINI_API_KEY:
        return

    async with session_factory() as session:
        result = await session.execute(
            select(func.count(Vocabulary.word_id)).where(and_(
                Vocabulary.is_active == True,
                Vocabulary.example_sentence_arabic == None,
                Vocabulary.category.notin_(["harf", "harakat"]),
            ))
        )
        missing = result.scalar() or 0

    if missing > 0:
        logger.info(f"Auto-generating {missing} example sentences via Gemini REST...")
        for admin_id in settings.ADMIN_IDS:
            try:
                await bot.send_message(
                    admin_id,
                    f"🤖 Gemini: {missing} ta so'z uchun misol jumlalar yaratilmoqda.\n"
                    f"Dars mashqlari boyib boradi!"
                )
            except Exception:
                pass
        asyncio.create_task(
            bulk_generate_missing(session_factory, bot, settings.ADMIN_IDS[0])
        )
