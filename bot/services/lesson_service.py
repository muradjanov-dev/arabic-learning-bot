import random
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.repository import VocabularyRepository
from bot.config import settings


QUESTION_TYPES = ["visual_match", "audio_match", "jumbled_sentence"]


async def build_lesson_questions(
    session: AsyncSession, user_id: int, level_id: int
) -> List[Dict[str, Any]]:
    vocab_repo = VocabularyRepository(session)
    words = await vocab_repo.get_for_lesson(user_id, level_id, settings.QUESTIONS_PER_LESSON)

    if not words:
        return []

    questions = []
    for word in words:
        wrong_options = await vocab_repo.get_random_wrong_translations(word.word_id, count=2)
        options = wrong_options + [word.uzbek_translation]
        random.shuffle(options)
        correct_index = options.index(word.uzbek_translation)

        # Decide question type — audio_match always available via on-the-fly TTS
        qtype = random.choice(["visual_match", "audio_match", "jumbled_sentence"])

        # For jumbled sentence, build the shuffled words list from the arabic word
        jumbled_words = []
        if qtype == "jumbled_sentence" and word.example_sentence_arabic:
            jumbled_words = word.example_sentence_arabic.split()
            random.shuffle(jumbled_words)
        elif qtype == "jumbled_sentence":
            qtype = "visual_match"

        questions.append({
            "word_id": word.word_id,
            "type": qtype,
            "arabic_word": word.arabic_word,
            "uzbek_translation": word.uzbek_translation,
            "transliteration": word.transliteration or "",
            "options": options,
            "correct_index": correct_index,
            "jumbled_words": jumbled_words,
            "jumbled_correct": word.example_sentence_arabic.split() if word.example_sentence_arabic else [],
            "sentence_uzbek": word.example_sentence_uzbek or "",
            "photo_file_id": word.telegram_photo_file_id,
            "audio_file_id": word.telegram_audio_file_id,
        })

    return questions
