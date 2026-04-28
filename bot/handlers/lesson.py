import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.database.repository import UserRepository, LessonRepository, ProgressRepository
from bot.keyboards.main_kb import confirm_lesson_kb, upsell_kb, main_menu_kb
from bot.keyboards.lesson_kb import (
    choice_question_kb, jumbled_kb, next_question_kb, lesson_result_kb,
    AnswerCb, JumbledWordCb, JumbledActionCb,
)
from bot.services.lesson_service import build_lesson_questions
from bot.services.gamification import calculate_xp, update_streak, tier_display
from bot.services.tts import get_audio_input_file, cache_audio_file_id
from bot.utils.messages import (
    LESSON_START_CONFIRM, LESSON_COMPLETE,
    QUESTION_VISUAL, QUESTION_AUDIO, QUESTION_JUMBLED,
    JUMBLED_SELECTED, JUMBLED_EMPTY,
    CORRECT_ANSWER, WRONG_ANSWER, NO_SHIJOAT, MAIN_MENU,
)
from bot.utils.praise import get_praise

logger = logging.getLogger(__name__)
router = Router()


class LessonStates(StatesGroup):
    in_lesson = State()
    answering = State()


# ── Lesson entry ──────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:lesson")
async def lesson_menu(callback: CallbackQuery, user):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return

    if user.shijoat_points < settings.LESSON_SHIJOAT_COST:
        await callback.message.edit_text(NO_SHIJOAT, reply_markup=upsell_kb())
        await callback.answer()
        return

    text = LESSON_START_CONFIRM.format(
        questions=settings.QUESTIONS_PER_LESSON,
        cost=settings.LESSON_SHIJOAT_COST,
        shijoat=user.shijoat_points,
    )
    await callback.message.edit_text(text, reply_markup=confirm_lesson_kb(user.shijoat_points))
    await callback.answer()


@router.callback_query(F.data == "lesson:start")
async def lesson_start(callback: CallbackQuery, state: FSMContext, user, session: AsyncSession):
    if user.shijoat_points < settings.LESSON_SHIJOAT_COST:
        await callback.answer("Shijoatingiz yetarli emas!", show_alert=True)
        return

    questions = await build_lesson_questions(session, user.user_id, user.current_level)
    if not questions:
        await callback.message.edit_text(
            "Bu darajada so'zlar topilmadi. Admin so'z qo'shishi kutilmoqda.",
            reply_markup=main_menu_kb(),
        )
        await callback.answer()
        return

    lesson_repo = LessonRepository(session)
    lesson = await lesson_repo.create(user.user_id, user.current_level)

    user_repo = UserRepository(session)
    await user_repo.update(
        user.user_id,
        shijoat_points=user.shijoat_points - settings.LESSON_SHIJOAT_COST,
        last_active_date=datetime.utcnow(),
    )

    await state.set_state(LessonStates.in_lesson)
    await state.set_data({
        "lesson_id": lesson.id,
        "questions": questions,
        "current_idx": 0,
        "correct_count": 0,
        "selected_words": [],
        "awaiting_next": False,
    })

    await callback.answer()
    await _send_question(callback.message, state, questions[0], edit=True, session=session)


# ── Question rendering ────────────────────────────────────────────────────────

async def _send_question(
    msg_or_target,
    state: FSMContext,
    q: dict,
    edit: bool = False,
    session: AsyncSession = None,
):
    data = await state.get_data()
    idx = data["current_idx"]
    total = len(data["questions"])
    header = f"📝 Savol {idx + 1}/{total}\n\n"

    qtype = q["type"]

    if qtype == "visual_match":
        text = header + QUESTION_VISUAL.format(arabic=q["arabic_word"])
        kb = choice_question_kb(q["options"], q["correct_index"])
        if q.get("photo_file_id"):
            if edit:
                await msg_or_target.edit_text(text, reply_markup=kb)
            else:
                await msg_or_target.answer_photo(
                    photo=q["photo_file_id"], caption=text, reply_markup=kb
                )
        else:
            if edit:
                await msg_or_target.edit_text(text, reply_markup=kb)
            else:
                await msg_or_target.answer(text, reply_markup=kb)

    elif qtype == "audio_match":
        text = header + QUESTION_AUDIO
        kb = choice_question_kb(q["options"], q["correct_index"])
        if edit:
            await msg_or_target.edit_text(text)
        else:
            await msg_or_target.answer(text)

        # Send audio: prefer cached file_id, otherwise generate via gTTS
        cached_file_id = q.get("audio_file_id")
        sent_voice = None
        if cached_file_id:
            try:
                sent_voice = await msg_or_target.answer_voice(voice=cached_file_id, reply_markup=kb)
            except Exception as e:
                logger.warning(f"Cached audio failed, regenerating: {e}")
                cached_file_id = None

        if not cached_file_id:
            audio_file = await get_audio_input_file(q["arabic_word"], q["word_id"])
            if audio_file:
                try:
                    sent_voice = await msg_or_target.answer_voice(voice=audio_file, reply_markup=kb)
                    new_file_id = sent_voice.voice.file_id if sent_voice and sent_voice.voice else None
                    if new_file_id and session is not None:
                        await cache_audio_file_id(session, q["word_id"], new_file_id)
                        # Update in-memory question dict so future renders use cache
                        q["audio_file_id"] = new_file_id
                except Exception as e:
                    logger.error(f"Sending TTS audio failed: {e}")
                    await msg_or_target.answer(f"🔊 <b>{q['arabic_word']}</b>", reply_markup=kb)
            else:
                # Fallback: just show the word as text
                await msg_or_target.answer(f"🔊 <b>{q['arabic_word']}</b>", reply_markup=kb)

    elif qtype == "jumbled_sentence":
        sentence_uzbek = q.get("sentence_uzbek") or q["uzbek_translation"]
        text = header + QUESTION_JUMBLED.format(uzbek=sentence_uzbek)
        selected = data.get("selected_words", [])
        selected_text = " ".join(q["jumbled_words"][i] for i in selected) if selected else JUMBLED_EMPTY
        text += f"\n\n{JUMBLED_SELECTED.format(words=selected_text)}"
        kb = jumbled_kb(q["jumbled_words"], selected)
        if edit:
            await msg_or_target.edit_text(text, reply_markup=kb)
        else:
            await msg_or_target.answer(text, reply_markup=kb)


# ── Answer handling: choice questions ────────────────────────────────────────

@router.callback_query(LessonStates.in_lesson, AnswerCb.filter())
async def handle_choice_answer(callback: CallbackQuery, callback_data: AnswerCb, state: FSMContext, session: AsyncSession, user):
    data = await state.get_data()
    if data.get("awaiting_next"):
        await callback.answer()
        return

    questions = data["questions"]
    idx = data["current_idx"]
    q = questions[idx]

    is_correct = callback_data.index == q["correct_index"]
    xp = settings.XP_PER_CORRECT if is_correct else 0

    prog_repo = ProgressRepository(session)
    await prog_repo.record_answer(user.user_id, q["word_id"], is_correct)

    if is_correct:
        feedback = CORRECT_ANSWER.format(xp=xp)
        await callback.answer(f"✅ To'g'ri! +{xp} XP", show_alert=False)
    else:
        feedback = WRONG_ANSWER.format(correct=q["uzbek_translation"])
        await callback.answer(f"❌ To'g'ri javob: {q['uzbek_translation']}", show_alert=True)

    new_correct = data["correct_count"] + (1 if is_correct else 0)
    await state.update_data(correct_count=new_correct, awaiting_next=True)

    text = callback.message.text or ""
    await callback.message.edit_text(
        text + f"\n\n{feedback}",
        reply_markup=next_question_kb(),
    )


# ── Answer handling: jumbled sentence ────────────────────────────────────────

@router.callback_query(LessonStates.in_lesson, JumbledWordCb.filter())
async def handle_jumbled_word(callback: CallbackQuery, callback_data: JumbledWordCb, state: FSMContext, session: AsyncSession, user):
    data = await state.get_data()
    selected = list(data.get("selected_words", []))

    if callback_data.word_index not in selected:
        selected.append(callback_data.word_index)
        await state.update_data(selected_words=selected)

    await callback.answer()
    questions = data["questions"]
    q = questions[data["current_idx"]]
    await _send_question(callback.message, state, q, edit=True, session=session)


@router.callback_query(LessonStates.in_lesson, JumbledActionCb.filter())
async def handle_jumbled_action(callback: CallbackQuery, callback_data: JumbledActionCb, state: FSMContext, session: AsyncSession, user):
    data = await state.get_data()
    if data.get("awaiting_next"):
        await callback.answer()
        return

    if callback_data.action == "reset":
        await state.update_data(selected_words=[])
        await callback.answer("Tozalandi")
        q = data["questions"][data["current_idx"]]
        await _send_question(callback.message, state, q, edit=True, session=session)
        return

    # Submit
    selected = data.get("selected_words", [])
    q = data["questions"][data["current_idx"]]
    selected_words = [q["jumbled_words"][i] for i in selected]
    correct_order = q.get("jumbled_correct", [])

    is_correct = selected_words == correct_order

    prog_repo = ProgressRepository(session)
    await prog_repo.record_answer(user.user_id, q["word_id"], is_correct)

    xp = settings.XP_PER_CORRECT if is_correct else 0
    new_correct = data["correct_count"] + (1 if is_correct else 0)
    await state.update_data(correct_count=new_correct, awaiting_next=True)

    if is_correct:
        feedback = CORRECT_ANSWER.format(xp=xp)
        await callback.answer(f"✅ To'g'ri!", show_alert=False)
    else:
        correct_str = " ".join(correct_order)
        feedback = WRONG_ANSWER.format(correct=correct_str)
        await callback.answer(f"❌ To'g'ri javob: {correct_str}", show_alert=True)

    text = callback.message.text or ""
    await callback.message.edit_text(
        text + f"\n\n{feedback}",
        reply_markup=next_question_kb(),
    )


# ── Next question ─────────────────────────────────────────────────────────────

@router.callback_query(LessonStates.in_lesson, F.data == "lesson:next")
async def lesson_next(callback: CallbackQuery, state: FSMContext, session: AsyncSession, user):
    data = await state.get_data()
    questions = data["questions"]
    next_idx = data["current_idx"] + 1

    await state.update_data(current_idx=next_idx, selected_words=[], awaiting_next=False)

    if next_idx >= len(questions):
        await _finish_lesson(callback, state, session, user)
        return

    await callback.answer()
    await _send_question(callback.message, state, questions[next_idx], edit=True, session=session)


# ── Lesson finish ─────────────────────────────────────────────────────────────

async def _finish_lesson(callback: CallbackQuery, state: FSMContext, session: AsyncSession, user):
    data = await state.get_data()
    correct = data["correct_count"]
    total = len(data["questions"])
    lesson_id = data["lesson_id"]

    # Update streak
    new_streak, streak_changed = update_streak(user)
    xp_earned, streak_bonus = calculate_xp(correct, total, new_streak)

    user_repo = UserRepository(session)
    await user_repo.update(
        user.user_id,
        current_xp=user.current_xp + xp_earned,
        streak_days=new_streak,
        last_active_date=datetime.utcnow(),
    )

    lesson_repo = LessonRepository(session)
    await lesson_repo.complete(lesson_id, correct, xp_earned)

    await state.clear()

    summary = LESSON_COMPLETE.format(
        correct=correct, total=total, xp=xp_earned, streak=new_streak
    )
    praise = get_praise(correct, total, new_streak, streak_bonus)

    await callback.message.edit_text(
        f"{summary}\n\n{praise}",
        reply_markup=lesson_result_kb(),
    )
    await callback.answer()
