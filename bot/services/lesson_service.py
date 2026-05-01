import random
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import UserProgress, Vocabulary
from bot.database.repository import VocabularyRepository

LETTER_CATEGORIES = {"harf", "harakat"}
NEW_PER_LESSON = 7     # max new words from current topic per lesson
REVIEW_PER_LESSON = 3  # SRS review words from previous topics
TOTAL_PER_LESSON = 10  # total questions per lesson
TOPIC_MASTERY = 3      # mastery_level >= this to count word as "done" in topic


async def build_lesson_questions(
    session: AsyncSession,
    user_id: int,
    level_id: int,
    current_topic: int,
) -> List[Dict[str, Any]]:
    vocab_repo = VocabularyRepository(session)

    # ── Step 1: load current topic words ─────────────────────────────────────
    topic_words = await vocab_repo.get_words_for_topic(level_id, current_topic)
    if not topic_words:
        topic_words = await vocab_repo.get_by_level(level_id)
    if not topic_words:
        return []

    topic_ids = [w.word_id for w in topic_words]

    # ── Step 2: check user progress on topic ─────────────────────────────────
    prog_result = await session.execute(
        select(UserProgress.word_id, UserProgress.mastery_level, UserProgress.next_review_date)
        .where(and_(UserProgress.user_id == user_id, UserProgress.word_id.in_(topic_ids)))
    )
    topic_progress = {r[0]: {"mastery": r[1], "next_review": r[2]} for r in prog_result.fetchall()}

    # New = not seen yet or mastery below threshold
    new_words = [w for w in topic_words if topic_progress.get(w.word_id, {}).get("mastery", 0) < TOPIC_MASTERY]
    random.shuffle(new_words)
    selected_new = new_words[:NEW_PER_LESSON]

    # ── Step 3: SRS review from previous topics ───────────────────────────────
    now = datetime.utcnow()
    review_result = await session.execute(
        select(Vocabulary)
        .join(UserProgress, and_(
            UserProgress.word_id == Vocabulary.word_id,
            UserProgress.user_id == user_id,
            UserProgress.next_review_date <= now,
        ))
        .where(and_(
            Vocabulary.is_active == True,
            ~Vocabulary.word_id.in_(topic_ids),
        ))
        .order_by(UserProgress.next_review_date.asc())
        .limit(REVIEW_PER_LESSON)
    )
    review_words = list(review_result.scalars().all())

    # ── Step 4: combine ───────────────────────────────────────────────────────
    combined = selected_new + review_words
    if not combined:
        combined = list(topic_words)

    # ── Step 5: always pad to TOTAL_PER_LESSON ───────────────────────────────
    # First pad with mastered words from current topic (good for retention)
    if len(combined) < TOTAL_PER_LESSON:
        selected_ids = {w.word_id for w in combined}
        extra_topic = [w for w in topic_words if w.word_id not in selected_ids]
        random.shuffle(extra_topic)
        combined += extra_topic[:TOTAL_PER_LESSON - len(combined)]

    # Then pad with any active words from current or earlier levels
    if len(combined) < TOTAL_PER_LESSON:
        needed = TOTAL_PER_LESSON - len(combined)
        selected_ids = {w.word_id for w in combined}
        fallback_result = await session.execute(
            select(Vocabulary)
            .where(and_(
                Vocabulary.is_active == True,
                Vocabulary.level_id <= level_id,
                ~Vocabulary.word_id.in_(selected_ids),
            ))
            .order_by(func.random())
            .limit(needed)
        )
        combined += list(fallback_result.scalars().all())

    random.shuffle(combined)
    words = combined[:TOTAL_PER_LESSON]

    seen_ids = set(topic_progress.keys())

    # ── Step 6: build question dicts ─────────────────────────────────────────
    questions: List[Dict[str, Any]] = []
    for word in words:
        is_new = word.word_id not in seen_ids
        category = word.category or ""

        tts_text = word.transliteration if (category in LETTER_CATEGORIES and word.transliteration) else word.arabic_word

        wrong_opts = await vocab_repo.get_random_wrong_translations(word.word_id, count=2)
        options = wrong_opts + [word.uzbek_translation]
        random.shuffle(options)
        correct_index = options.index(word.uzbek_translation)

        if category in LETTER_CATEGORIES:
            qtype = random.choice(["visual_match", "audio_match"])
        elif word.example_sentence_arabic:
            qtype = random.choice(["visual_match", "audio_match", "jumbled_sentence"])
        else:
            qtype = random.choice(["visual_match", "audio_match"])

        jumbled_words: list = []
        if qtype == "jumbled_sentence" and word.example_sentence_arabic:
            jumbled_words = word.example_sentence_arabic.split()
            random.shuffle(jumbled_words)

        questions.append({
            "word_id": word.word_id,
            "type": qtype,
            "arabic_word": word.arabic_word,
            "uzbek_translation": word.uzbek_translation,
            "transliteration": word.transliteration or "",
            "tts_text": tts_text,
            "is_new": is_new,
            "options": options,
            "correct_index": correct_index,
            "jumbled_words": jumbled_words,
            "jumbled_correct": word.example_sentence_arabic.split() if word.example_sentence_arabic else [],
            "sentence_uzbek": word.example_sentence_uzbek or "",
            "audio_file_id": word.telegram_audio_file_id,
        })

    return questions


async def check_topic_complete(
    session: AsyncSession,
    user_id: int,
    level_id: int,
    topic_id: int,
) -> bool:
    """True when every word in this topic has mastery_level >= TOPIC_MASTERY."""
    vocab_repo = VocabularyRepository(session)
    words = await vocab_repo.get_words_for_topic(level_id, topic_id)
    if not words:
        return True
    word_ids = [w.word_id for w in words]
    result = await session.execute(
        select(func.count(UserProgress.id)).where(and_(
            UserProgress.user_id == user_id,
            UserProgress.word_id.in_(word_ids),
            UserProgress.mastery_level >= TOPIC_MASTERY,
        ))
    )
    return (result.scalar() or 0) >= len(words)
