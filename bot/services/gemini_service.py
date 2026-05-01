"""
Gemini AI content generation — runs ONCE per vocabulary word, cached in DB.
All users read from DB; no AI calls happen during lessons.
"""
import asyncio
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Gemini RPM limit on free tier: 15 req/min → 4 second delay between calls
_REQUEST_DELAY = 4.5


def _build_prompt(arabic_word: str, uzbek_translation: str, transliteration: str, level_id: int) -> str:
    if level_id <= 2:
        complexity = "very simple — just THIS word used alone or with 1 known word like هذا/هي"
    elif level_id <= 4:
        complexity = "simple — 2 to 4 words, subject + this word"
    elif level_id <= 6:
        complexity = "moderate — 4 to 6 words, simple subject + verb + this word"
    else:
        complexity = "natural — 5 to 8 words, complete meaningful sentence"

    return f"""You are an Arabic teacher creating exercises for Uzbek-speaking beginner students.

Arabic word: {arabic_word}
Uzbek meaning: {uzbek_translation}
Pronunciation: {transliteration}
Level: {level_id}/10 — complexity: {complexity}

Create ONE example Arabic sentence that:
- Uses this exact word (not a derivative)
- Follows the complexity guideline above
- Uses Modern Standard Arabic (Fusha)
- Is grammatically correct with full diacritics (harakat)
- Translates naturally into Uzbek

Return ONLY valid JSON (no markdown, no explanation):
{{"arabic": "الجملة هنا", "uzbek": "O'zbek tarjimasi"}}"""


async def generate_example_sentence(
    arabic_word: str,
    uzbek_translation: str,
    transliteration: str,
    level_id: int,
) -> Optional[dict]:
    """Call Gemini once for one word. Returns {arabic, uzbek} or None."""
    from bot.config import settings
    if not settings.GEMINI_API_KEY:
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = _build_prompt(arabic_word, uzbek_translation, transliteration or "", level_id)

        response = await asyncio.to_thread(model.generate_content, prompt)
        raw = response.text.strip()

        # Strip markdown code fences if present
        if "```" in raw:
            parts = raw.split("```")
            raw = parts[1] if len(parts) > 1 else raw
            if raw.startswith("json"):
                raw = raw[4:].strip()

        data = json.loads(raw)
        if isinstance(data, dict) and "arabic" in data and "uzbek" in data:
            return {"arabic": data["arabic"].strip(), "uzbek": data["uzbek"].strip()}
    except Exception as e:
        logger.error(f"Gemini failed for '{arabic_word}': {e}")
    return None


async def bulk_generate_missing(
    session_factory,
    bot,
    admin_chat_id: int,
    level_filter: Optional[int] = None,
) -> None:
    """
    Background task: find all vocabulary words with no example sentence,
    call Gemini for each, save to DB. Runs once; all users share the result.
    """
    from sqlalchemy import select, and_, update
    from bot.database.models import Vocabulary

    async with session_factory() as session:
        q = select(Vocabulary).where(
            and_(
                Vocabulary.is_active == True,
                Vocabulary.example_sentence_arabic == None,
                Vocabulary.category.notin_(["harf", "harakat"]),
            )
        ).order_by(Vocabulary.level_id, Vocabulary.topic_id)
        if level_filter:
            q = q.where(Vocabulary.level_id == level_filter)
        result = await session.execute(q)
        words = result.scalars().all()

    if not words:
        try:
            await bot.send_message(admin_chat_id, "✅ Barcha so'zlarda misol jumlalar mavjud.")
        except Exception:
            pass
        return

    total = len(words)
    try:
        status_msg = await bot.send_message(
            admin_chat_id,
            f"⏳ {total} ta so'z uchun jumlalar yaratilmoqda...\n(~{total * _REQUEST_DELAY / 60:.0f} daqiqa)"
        )
        status_id = status_msg.message_id
    except Exception:
        status_id = None

    done = 0
    failed = 0

    for word in words:
        result = await generate_example_sentence(
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
            failed += 1

        # Update status every 10 words
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

    summary = f"✅ Yaratish yakunlandi!\n\n✅ Muvaffaqiyatli: {done}\n❌ Xatolik: {failed}\nJami: {total}"
    try:
        if status_id:
            await bot.edit_message_text(summary, chat_id=admin_chat_id, message_id=status_id)
        else:
            await bot.send_message(admin_chat_id, summary)
    except Exception:
        pass
    logger.info(f"Gemini bulk generation done: {done}/{total} words.")


async def auto_generate_on_startup(session_factory, bot) -> None:
    """Called at startup: if GEMINI_API_KEY set and words are missing, notify admin."""
    from bot.config import settings
    from bot.database.models import Vocabulary
    from sqlalchemy import select, and_, func

    if not settings.GEMINI_API_KEY:
        return

    async with session_factory() as session:
        result = await session.execute(
            select(func.count(Vocabulary.word_id)).where(
                and_(
                    Vocabulary.is_active == True,
                    Vocabulary.example_sentence_arabic == None,
                    Vocabulary.category.notin_(["harf", "harakat"]),
                )
            )
        )
        missing = result.scalar() or 0

    if missing > 0:
        logger.info(f"Auto-generating {missing} missing example sentences via Gemini...")
        for admin_id in settings.ADMIN_IDS:
            try:
                await bot.send_message(
                    admin_id,
                    f"🤖 Gemini: {missing} ta so'z uchun misol jumlalar yaratish boshlandi.\n"
                    f"Dars sifati yaxshilanadi. /genwords cancel uchun."
                )
            except Exception:
                pass
        asyncio.create_task(bulk_generate_missing(session_factory, bot, settings.ADMIN_IDS[0]))
