import asyncio
import logging
import random
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.database.repository import UserRepository, LessonRepository, ProgressRepository
from bot.keyboards.main_kb import confirm_lesson_kb, upsell_kb, main_menu_kb
from bot.keyboards.lesson_kb import (
    choice_question_kb, jumbled_kb, lesson_result_kb,
    AnswerCb, JumbledWordCb, JumbledActionCb,
)
from bot.services.lesson_service import build_lesson_questions
from bot.services.gamification import calculate_xp, update_streak
from bot.services.tts import get_audio_input_file, cache_audio_file_id
from bot.utils.messages import (
    LESSON_START_CONFIRM, LESSON_COMPLETE,
    QUESTION_VISUAL, QUESTION_AUDIO, QUESTION_JUMBLED,
    JUMBLED_SELECTED, JUMBLED_EMPTY,
    QUESTION_HEADER, QUESTION_HEADER_NEW,
    NEW_WORD_INTRO, PROGRESS_PIN,
    CORRECT_MOTIVATIONS, WRONG_HINTS,
    NO_SHIJOAT,
)
from bot.utils.praise import get_praise

logger = logging.getLogger(__name__)
router = Router()


class LessonStates(StatesGroup):
    in_lesson = State()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _progress_bar(current: int, total: int) -> str:
    filled = int((current / total) * 10) if total else 0
    return "█" * filled + "░" * (10 - filled)


async def _update_pin(bot: Bot, chat_id: int, pin_msg_id: int, current: int, total: int):
    pct = int((current / total) * 100) if total else 0
    bar = _progress_bar(current, total)
    try:
        await bot.edit_message_text(
            text=PROGRESS_PIN.format(bar=bar, pct=pct, current=current, total=total),
            chat_id=chat_id,
            message_id=pin_msg_id,
        )
    except Exception:
        pass


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

    new_shijoat = user.shijoat_points - settings.LESSON_SHIJOAT_COST
    user_repo = UserRepository(session)
    await user_repo.update(
        user.user_id,
        shijoat_points=new_shijoat,
        last_active_date=datetime.utcnow(),
    )

    total = len(questions)
    # Pin a progress message
    pin_msg = await callback.message.answer(
        PROGRESS_PIN.format(bar=_progress_bar(0, total), pct=0, current=0, total=total)
    )
    chat_id = callback.message.chat.id
    try:
        await callback.bot.pin_chat_message(
            chat_id=chat_id, message_id=pin_msg.message_id, disable_notification=True
        )
    except Exception:
        pass

    await state.set_state(LessonStates.in_lesson)
    await state.set_data({
        "lesson_id": lesson.id,
        "questions": questions,
        "current_idx": 0,
        "correct_count": 0,
        "selected_words": [],
        "shijoat": new_shijoat,
        "pin_msg_id": pin_msg.message_id,
        "chat_id": chat_id,
    })

    await callback.answer()
    await _send_question(callback.message, state, questions[0], edit=True, session=session)


# ── Question rendering ────────────────────────────────────────────────────────

async def _send_question(
    msg: Message,
    state: FSMContext,
    q: dict,
    edit: bool = False,
    session: AsyncSession = None,
):
    data = await state.get_data()
    idx = data["current_idx"]
    total = len(data["questions"])
    shijoat = data.get("shijoat", 0)

    if q.get("is_new"):
        header = QUESTION_HEADER_NEW.format(idx=idx + 1, total=total, shijoat=shijoat)
        new_intro = NEW_WORD_INTRO.format(arabic=q["arabic_word"], uzbek=q["uzbek_translation"]) + "\n\n"
    else:
        header = QUESTION_HEADER.format(idx=idx + 1, total=total, shijoat=shijoat)
        new_intro = ""

    qtype = q["type"]

    if qtype == "visual_match":
        text = header + "\n\n" + new_intro + QUESTION_VISUAL.format(arabic=q["arabic_word"])
        kb = choice_question_kb(q["options"], q["correct_index"])
        if edit:
            await msg.edit_text(text, reply_markup=kb)
        else:
            await msg.answer(text, reply_markup=kb)

    elif qtype == "audio_match":
        text = header + "\n\n" + new_intro + QUESTION_AUDIO
        kb = choice_question_kb(q["options"], q["correct_index"])

        # Send text prompt (edit or new)
        if edit:
            try:
                await msg.edit_text(text)
            except Exception:
                await msg.answer(text)
        else:
            await msg.answer(text)

        # Send voice with keyboard
        tts_text = q.get("tts_text") or q["arabic_word"]
        cached_id = q.get("audio_file_id")
        sent_voice = None

        if cached_id:
            try:
                sent_voice = await msg.answer_voice(voice=cached_id, reply_markup=kb)
            except Exception:
                cached_id = None

        if not cached_id:
            audio_file = await get_audio_input_file(tts_text, q["word_id"])
            if audio_file:
                try:
                    sent_voice = await msg.answer_voice(voice=audio_file, reply_markup=kb)
                    new_fid = sent_voice.voice.file_id if sent_voice and sent_voice.voice else None
                    if new_fid and session:
                        await cache_audio_file_id(session, q["word_id"], new_fid)
                        q["audio_file_id"] = new_fid
                except Exception as e:
                    logger.error(f"TTS send failed: {e}")
                    await msg.answer(f"🔊 <b>{q['arabic_word']}</b>", reply_markup=kb)
            else:
                await msg.answer(f"🔊 <b>{q['arabic_word']}</b>", reply_markup=kb)

    elif qtype == "jumbled_sentence":
        sentence_uzbek = q.get("sentence_uzbek") or q["uzbek_translation"]
        selected = data.get("selected_words", [])
        selected_text = (
            " ".join(q["jumbled_words"][i] for i in selected) if selected else None
        )
        answer_block = (
            JUMBLED_SELECTED.format(words=selected_text)
            if selected_text
            else JUMBLED_EMPTY
        )
        text = header + "\n\n" + new_intro + QUESTION_JUMBLED.format(uzbek=sentence_uzbek) + "\n\n" + answer_block
        kb = jumbled_kb(q["jumbled_words"], selected)
        if edit:
            await msg.edit_text(text, reply_markup=kb)
        else:
            await msg.answer(text, reply_markup=kb)


# ── Auto-advance helper ───────────────────────────────────────────────────────

async def _advance(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user,
    is_voice: bool,
):
    """Remove keyboard, wait briefly, then send next question or finish."""
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await asyncio.sleep(1.0)

    data = await state.get_data()
    next_idx = data["current_idx"] + 1
    questions = data["questions"]

    await state.update_data(current_idx=next_idx, selected_words=[])

    # Update pinned progress
    pin_id = data.get("pin_msg_id")
    chat_id = data.get("chat_id")
    if pin_id and chat_id:
        await _update_pin(callback.bot, chat_id, pin_id, next_idx, len(questions))

    if next_idx >= len(questions):
        await _finish_lesson(callback, state, session, user)
        return

    # For voice messages we can't edit to text — always send new message
    await _send_question(
        callback.message, state, questions[next_idx],
        edit=(not is_voice),
        session=session,
    )


# ── Answer handling: choice questions ────────────────────────────────────────

@router.callback_query(LessonStates.in_lesson, AnswerCb.filter())
async def handle_choice_answer(
    callback: CallbackQuery, callback_data: AnswerCb,
    state: FSMContext, session: AsyncSession, user,
):
    data = await state.get_data()
    questions = data["questions"]
    idx = data["current_idx"]
    q = questions[idx]

    is_correct = callback_data.index == q["correct_index"]
    xp = settings.XP_PER_CORRECT if is_correct else 0

    prog_repo = ProgressRepository(session)
    await prog_repo.record_answer(user.user_id, q["word_id"], is_correct)

    new_correct = data["correct_count"] + (1 if is_correct else 0)
    await state.update_data(correct_count=new_correct)

    if is_correct:
        await callback.answer(random.choice(CORRECT_MOTIVATIONS), show_alert=False)
    else:
        hint = random.choice(WRONG_HINTS)
        await callback.answer(f"❌ {hint} {q['uzbek_translation']}", show_alert=True)

    is_voice = callback.message.voice is not None
    await _advance(callback, state, session, user, is_voice)


# ── Answer handling: jumbled sentence ────────────────────────────────────────

@router.callback_query(LessonStates.in_lesson, JumbledWordCb.filter())
async def handle_jumbled_word(
    callback: CallbackQuery, callback_data: JumbledWordCb,
    state: FSMContext, session: AsyncSession, user,  # noqa: ARG001
):
    data = await state.get_data()
    selected = list(data.get("selected_words", []))

    if callback_data.word_index not in selected:
        selected.append(callback_data.word_index)
        await state.update_data(selected_words=selected)

    await callback.answer()
    q = data["questions"][data["current_idx"]]
    await _send_question(callback.message, state, q, edit=True, session=session)


@router.callback_query(LessonStates.in_lesson, JumbledActionCb.filter())
async def handle_jumbled_action(
    callback: CallbackQuery, callback_data: JumbledActionCb,
    state: FSMContext, session: AsyncSession, user,
):
    data = await state.get_data()

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

    new_correct = data["correct_count"] + (1 if is_correct else 0)
    await state.update_data(correct_count=new_correct)

    if is_correct:
        await callback.answer(random.choice(CORRECT_MOTIVATIONS), show_alert=False)
    else:
        correct_str = " ".join(correct_order)
        hint = random.choice(WRONG_HINTS)
        await callback.answer(f"❌ {hint} {correct_str}", show_alert=True)

    await _advance(callback, state, session, user, is_voice=False)


# ── Lesson finish ─────────────────────────────────────────────────────────────

async def _finish_lesson(callback: CallbackQuery, state: FSMContext, session: AsyncSession, user):
    data = await state.get_data()
    correct = data["correct_count"]
    questions = data["questions"]
    total = len(questions)
    lesson_id = data["lesson_id"]

    new_streak, _ = update_streak(user)
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

    # Unpin and update progress message
    pin_id = data.get("pin_msg_id")
    chat_id = data.get("chat_id")
    if pin_id and chat_id:
        try:
            await callback.bot.edit_message_text(
                "✅ Dars yakunlandi!", chat_id=chat_id, message_id=pin_id
            )
            await callback.bot.unpin_chat_message(chat_id=chat_id, message_id=pin_id)
        except Exception:
            pass

    await state.clear()

    summary = LESSON_COMPLETE.format(correct=correct, total=total, xp=xp_earned, streak=new_streak)
    praise = get_praise(correct, total, new_streak, streak_bonus)

    try:
        await callback.message.edit_text(f"{summary}\n\n{praise}", reply_markup=lesson_result_kb())
    except Exception:
        await callback.message.answer(f"{summary}\n\n{praise}", reply_markup=lesson_result_kb())

    await callback.answer()
