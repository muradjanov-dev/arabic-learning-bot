import random
from typing import List, Dict, Any
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.repository import VocabularyRepository
from bot.database.models import UserProgress
from bot.config import settings

LETTER_CATEGORIES = {"harf", "harakat"}


async def build_lesson_questions(
    session: AsyncSession, user_id: int, level_id: int
) -> List[Dict[str, Any]]:
    vocab_repo = VocabularyRepository(session)
    words = await vocab_repo.get_for_lesson(user_id, level_id, settings.QUESTIONS_PER_LESSON)

    if not words:
        return []

    word_ids = [w.word_id for w in words]

    # Determine which words the user has seen before
    seen_result = await session.execute(
        select(UserProgress.word_id).where(
            and_(UserProgress.user_id == user_id, UserProgress.word_id.in_(word_ids))
        )
    )
    seen_ids = {row[0] for row in seen_result.fetchall()}

    questions = []
    for word in words:
        is_new = word.word_id not in seen_ids
        category = word.category or ""

        # For letters/harakats, TTS speaks the letter name (transliteration)
        if category in LETTER_CATEGORIES and word.transliteration:
            tts_text = word.transliteration
        else:
            tts_text = word.arabic_word

        wrong_options = await vocab_repo.get_random_wrong_translations(word.word_id, count=2)
        options = wrong_options + [word.uzbek_translation]
        random.shuffle(options)
        correct_index = options.index(word.uzbek_translation)

        # Letters/harakats only support visual/audio (no sentence to jumble)
        if category in LETTER_CATEGORIES:
            qtype = random.choice(["visual_match", "audio_match"])
        elif word.example_sentence_arabic:
            qtype = random.choice(["visual_match", "audio_match", "jumbled_sentence"])
        else:
            qtype = random.choice(["visual_match", "audio_match"])

        jumbled_words = []
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
            "photo_file_id": word.telegram_photo_file_id,
            "audio_file_id": word.telegram_audio_file_id,
        })

    return questions
