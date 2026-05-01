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
from bot.database.repository import UserRepository, LessonRepository, ProgressRepository, VocabularyRepository
from bot.keyboards.main_kb import confirm_lesson_kb, upsell_kb, main_menu_kb, congrat_kb
from bot.keyboards.lesson_kb import (
    choice_question_kb, jumbled_kb, lesson_result_kb,
    AnswerCb, JumbledWordCb, JumbledActionCb,
)
from bot.services.lesson_service import build_lesson_questions, check_topic_complete
from bot.services.gamification import (
    calculate_xp, update_streak, check_new_achievements,
    ACHIEVEMENTS, shijoat_pin_text, TOPIC_NAMES,
)
from bot.services.tts import get_audio_input_file, cache_audio_file_id
from bot.utils.messages import (
    LESSON_START_CONFIRM, LESSON_COMPLETE, LEVEL_UP, TOPIC_UP, MODULE_UP,
    QUESTION_VISUAL, QUESTION_AUDIO, QUESTION_JUMBLED,
    JUMBLED_SELECTED, JUMBLED_EMPTY,
    QUESTION_HEADER, QUESTION_HEADER_NEW,
    NEW_WORD_INTRO, PROGRESS_PIN,
    CORRECT_MOTIVATIONS, WRONG_HINTS,
    NO_SHIJOAT, ACHIEVEMENT_EARNED,
    ACHIEVEMENT_BROADCAST, CONGRAT_SENT, CONGRAT_TOAST,
)
from bot.utils.praise import get_praise

logger = logging.getLogger(__name__)
router = Router()

MAX_LEVEL = 10


class LessonStates(StatesGroup):
    in_lesson = State()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _bar(current: int, total: int, width: int = 10) -> str:
    filled = int((current / total) * width) if total else 0
    return "█" * filled + "░" * (width - filled)


async def _update_pin(bot: Bot, chat_id: int, pin_msg_id: int, current: int, total: int) -> None:
    pct = int((current / total) * 100) if total else 0
    try:
        await bot.edit_message_text(
            text=PROGRESS_PIN.format(bar=_bar(current, total), pct=pct, current=current, total=total),
            chat_id=chat_id,
            message_id=pin_msg_id,
        )
    except Exception:
        pass


async def _try_delete(bot: Bot, chat_id: int, message_ids: list) -> None:
    for mid in message_ids:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=mid)
        except Exception:
            pass


async def _get_module_pct(session: AsyncSession, user) -> int:
    """Returns mastery % for the user's current topic."""
    from sqlalchemy import select, and_, func as sqlfunc
    from bot.database.models import UserProgress
    current_topic = getattr(user, "current_topic", 1)
    vocab_repo = VocabularyRepository(session)
    words = await vocab_repo.get_words_for_topic(user.current_level, current_topic)
    if not words:
        return 0
    ids = [w.word_id for w in words]
    r = await session.execute(
        select(sqlfunc.count(UserProgress.id)).where(and_(
            UserProgress.user_id == user.user_id,
            UserProgress.word_id.in_(ids),
            UserProgress.mastery_level >= 3,
        ))
    )
    return int((r.scalar() or 0) / len(words) * 100)


async def _update_shijoat_pin(bot: Bot, user, session: AsyncSession) -> None:
    if not getattr(user, "shijoat_pin_id", None):
        return
    pct = await _get_module_pct(session, user)
    text = shijoat_pin_text(
        user.shijoat_points,
        user.current_level,
        getattr(user, "current_topic", 1),
        pct,
        user.subscription_tier,
    )
    try:
        await bot.edit_message_text(text=text, chat_id=user.user_id, message_id=user.shijoat_pin_id)
    except Exception:
        pass


async def _broadcast_achievement(
    bot: Bot,
    session_factory,
    achiever_id: int,
    achiever_name: str,
    ach_key: str,
    ach_name: str,
    ach_desc: str,
) -> None:
    """Broadcast achievement to all users except achiever after a 2-second delay."""
    await asyncio.sleep(2)

    from bot.database.models import User
    from sqlalchemy import select

    async with session_factory() as session:
        try:
            result = await session.execute(
                select(User).where(
                    User.is_registered == True,
                    User.is_banned == False,
                    User.user_id != achiever_id,
                )
            )
            users = result.scalars().all()

            text = ACHIEVEMENT_BROADCAST.format(
                name=achiever_name,
                ach_name=ach_name,
                ach_desc=ach_desc,
            )
            kb = congrat_kb(achiever_id, ach_key)

            for u in users:
                try:
                    sent = await bot.send_message(u.user_id, text, reply_markup=kb)
                    # Schedule auto-delete after 5 minutes
                    asyncio.create_task(_delayed_delete(bot, u.user_id, sent.message_id, delay=300))
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Achievement broadcast failed: {e}")


async def _delayed_delete(bot: Bot, chat_id: int, message_id: int, delay: int = 300) -> None:
    """Delete a message after a delay in seconds."""
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass


# ── Lesson entry ──────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:lesson")
async def lesson_menu(callback: CallbackQuery, user, session: AsyncSession):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return

    if user.shijoat_points < settings.LESSON_SHIJOAT_COST:
        await callback.message.edit_text(NO_SHIJOAT, reply_markup=upsell_kb())
        await callback.answer()
        return

    current_topic = getattr(user, "current_topic", 1)
    vocab_repo = VocabularyRepository(session)
    topic_words = await vocab_repo.get_words_for_topic(user.current_level, current_topic)
    total_in_topic = max(len(topic_words), 1)

    from sqlalchemy import select, and_
    from bot.database.models import UserProgress
    if topic_words:
        ids = [w.word_id for w in topic_words]
        from sqlalchemy import func as sqlfunc
        r = await session.execute(
            select(sqlfunc.count(UserProgress.id)).where(and_(
                UserProgress.user_id == user.user_id,
                UserProgress.word_id.in_(ids),
                UserProgress.mastery_level >= 3,
            ))
        )
        mastered_in_topic = r.scalar() or 0
    else:
        mastered_in_topic = 0

    progress_pct = int(mastered_in_topic / total_in_topic * 100)

    from bot.services.lesson_service import TOTAL_PER_LESSON
    topic_name = TOPIC_NAMES.get((user.current_level, current_topic), f"Mavzu {current_topic}")
    text = LESSON_START_CONFIRM.format(
        module=user.current_level,
        topic=current_topic,
        topic_name=topic_name,
        questions=TOTAL_PER_LESSON,
        cost=settings.LESSON_SHIJOAT_COST,
        shijoat=user.shijoat_points,
        module_pct=progress_pct,
    )
    await callback.message.edit_text(text, reply_markup=confirm_lesson_kb(user.shijoat_points))
    await callback.answer()


@router.callback_query(F.data == "lesson:start")
async def lesson_start(callback: CallbackQuery, state: FSMContext, user, session: AsyncSession):
    if user.shijoat_points < settings.LESSON_SHIJOAT_COST:
        await callback.answer("Shijoatingiz yetarli emas!", show_alert=True)
        return

    current_topic = getattr(user, "current_topic", 1)
    questions = await build_lesson_questions(session, user.user_id, user.current_level, current_topic)
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
    await user_repo.update(user.user_id, shijoat_points=new_shijoat, last_active_date=datetime.utcnow())
    await session.commit()

    total = len(questions)
    chat_id = callback.message.chat.id

    # Reuse shijoat pin for progress — no new messages, no pin notifications
    shijoat_pin_id = getattr(user, "shijoat_pin_id", None)
    progress_text = PROGRESS_PIN.format(bar=_bar(0, total), pct=0, current=0, total=total)
    pin_msg_id = None

    if shijoat_pin_id:
        try:
            await callback.bot.edit_message_text(
                text=progress_text, chat_id=chat_id, message_id=shijoat_pin_id
            )
            pin_msg_id = shijoat_pin_id
        except Exception:
            pass
    # No fallback pin — never pin any message during a lesson

    await state.set_state(LessonStates.in_lesson)
    await state.set_data({
        "lesson_id": lesson.id,
        "questions": questions,
        "current_idx": 0,
        "correct_count": 0,
        "selected_words": [],
        "shijoat": new_shijoat,
        "pin_msg_id": pin_msg_id,
        "chat_id": chat_id,
        "msg_ids": [],
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
) -> None:
    data = await state.get_data()
    idx = data["current_idx"]
    total = len(data["questions"])
    correct_count = data.get("correct_count", 0)
    olmos = correct_count * 5  # XP_PER_CORRECT
    msg_ids = list(data.get("msg_ids", []))

    header = (
        QUESTION_HEADER_NEW.format(idx=idx + 1, total=total, olmos=olmos)
        if q.get("is_new")
        else QUESTION_HEADER.format(idx=idx + 1, total=total, olmos=olmos)
    )
    intro = (
        NEW_WORD_INTRO.format(arabic=q["arabic_word"], uzbek=q["uzbek_translation"]) + "\n"
        if q.get("is_new")
        else ""
    )

    qtype = q["type"]

    if qtype == "visual_match":
        text = f"{header}\n\n{intro}{QUESTION_VISUAL.format(arabic=q['arabic_word'])}"
        kb = choice_question_kb(q["options"], q["correct_index"])
        if edit:
            await msg.edit_text(text, reply_markup=kb)
        else:
            sent = await msg.answer(text, reply_markup=kb)
            msg_ids.append(sent.message_id)
            await state.update_data(msg_ids=msg_ids)

    elif qtype == "audio_match":
        text = f"{header}\n\n{intro}{QUESTION_AUDIO}"
        kb = choice_question_kb(q["options"], q["correct_index"])

        if edit:
            try:
                await msg.edit_text(text)
            except Exception:
                sent = await msg.answer(text)
                msg_ids.append(sent.message_id)
                await state.update_data(msg_ids=msg_ids)
        else:
            sent = await msg.answer(text)
            msg_ids.append(sent.message_id)
            await state.update_data(msg_ids=msg_ids)

        tts_text = q.get("tts_text") or q["arabic_word"]
        cached_id = q.get("audio_file_id")

        if cached_id:
            try:
                sent_v = await msg.answer_voice(voice=cached_id, reply_markup=kb)
                msg_ids.append(sent_v.message_id)
                await state.update_data(msg_ids=msg_ids)
            except Exception:
                cached_id = None

        if not cached_id:
            audio_file = await get_audio_input_file(tts_text, q["word_id"])
            if audio_file:
                try:
                    sent_v = await msg.answer_voice(voice=audio_file, reply_markup=kb)
                    msg_ids.append(sent_v.message_id)
                    await state.update_data(msg_ids=msg_ids)
                    new_fid = sent_v.voice.file_id if sent_v and sent_v.voice else None
                    if new_fid and session:
                        await cache_audio_file_id(session, q["word_id"], new_fid)
                        q["audio_file_id"] = new_fid
                except Exception as e:
                    logger.error(f"TTS send failed: {e}")
                    sent_fb = await msg.answer(f"🔊 <b>{q['arabic_word']}</b>", reply_markup=kb)
                    msg_ids.append(sent_fb.message_id)
                    await state.update_data(msg_ids=msg_ids)
            else:
                sent_fb = await msg.answer(f"🔊 <b>{q['arabic_word']}</b>", reply_markup=kb)
                msg_ids.append(sent_fb.message_id)
                await state.update_data(msg_ids=msg_ids)

    elif qtype == "jumbled_sentence":
        sentence_uzbek = q.get("sentence_uzbek") or q["uzbek_translation"]
        selected = data.get("selected_words", [])
        selected_text = " ".join(q["jumbled_words"][i] for i in selected) if selected else None
        answer_block = JUMBLED_SELECTED.format(words=selected_text) if selected_text else JUMBLED_EMPTY
        text = f"{header}\n\n{intro}{QUESTION_JUMBLED.format(uzbek=sentence_uzbek)}\n\n{answer_block}"
        kb = jumbled_kb(q["jumbled_words"], selected)
        if edit:
            await msg.edit_text(text, reply_markup=kb)
        else:
            sent = await msg.answer(text, reply_markup=kb)
            msg_ids.append(sent.message_id)
            await state.update_data(msg_ids=msg_ids)


# ── Auto-advance ──────────────────────────────────────────────────────────────

async def _advance(callback: CallbackQuery, state: FSMContext, session: AsyncSession, user, is_voice: bool) -> None:
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await asyncio.sleep(1.0)

    data = await state.get_data()
    next_idx = data["current_idx"] + 1
    questions = data["questions"]

    await state.update_data(current_idx=next_idx, selected_words=[])

    pin_id = data.get("pin_msg_id")
    chat_id = data.get("chat_id")
    if pin_id and chat_id:
        await _update_pin(callback.bot, chat_id, pin_id, next_idx, len(questions))

    if next_idx >= len(questions):
        await _finish_lesson(callback, state, session, user)
        return

    await _send_question(
        callback.message, state, questions[next_idx],
        edit=not is_voice, session=session,
    )


# ── Answer handlers ───────────────────────────────────────────────────────────

@router.callback_query(LessonStates.in_lesson, AnswerCb.filter())
async def handle_choice_answer(
    callback: CallbackQuery, callback_data: AnswerCb,
    state: FSMContext, session: AsyncSession, user,
):
    data = await state.get_data()
    q = data["questions"][data["current_idx"]]
    is_correct = callback_data.index == q["correct_index"]

    prog_repo = ProgressRepository(session)
    await prog_repo.record_answer(user.user_id, q["word_id"], is_correct)
    await session.commit()

    await state.update_data(correct_count=data["correct_count"] + (1 if is_correct else 0))

    if is_correct:
        await callback.answer(random.choice(CORRECT_MOTIVATIONS), show_alert=False)
    else:
        await callback.answer(f"❌ {random.choice(WRONG_HINTS)} {q['uzbek_translation']}", show_alert=True)

    await _advance(callback, state, session, user, is_voice=callback.message.voice is not None)


@router.callback_query(LessonStates.in_lesson, JumbledWordCb.filter())
async def handle_jumbled_word(
    callback: CallbackQuery, callback_data: JumbledWordCb,
    state: FSMContext, session: AsyncSession,
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

    selected = data.get("selected_words", [])
    q = data["questions"][data["current_idx"]]
    selected_words = [q["jumbled_words"][i] for i in selected]
    correct_order = q.get("jumbled_correct", [])
    is_correct = selected_words == correct_order

    prog_repo = ProgressRepository(session)
    await prog_repo.record_answer(user.user_id, q["word_id"], is_correct)
    await session.commit()

    await state.update_data(correct_count=data["correct_count"] + (1 if is_correct else 0))

    if is_correct:
        await callback.answer(random.choice(CORRECT_MOTIVATIONS), show_alert=False)
    else:
        await callback.answer(f"❌ {random.choice(WRONG_HINTS)} {' '.join(correct_order)}", show_alert=True)

    await _advance(callback, state, session, user, is_voice=False)


# ── Lesson finish ─────────────────────────────────────────────────────────────

async def _finish_lesson(callback: CallbackQuery, state: FSMContext, session: AsyncSession, user) -> None:
    data = await state.get_data()
    correct = data["correct_count"]
    questions = data["questions"]
    total = len(questions)
    lesson_id = data["lesson_id"]
    chat_id = data.get("chat_id")
    pin_id = data.get("pin_msg_id")
    msg_ids = data.get("msg_ids", [])

    new_streak, _ = update_streak(user)
    xp_earned, streak_bonus = calculate_xp(correct, total, new_streak)

    user_repo = UserRepository(session)
    prog_repo = ProgressRepository(session)

    # Increment daily_lessons_done
    current_daily = getattr(user, "daily_lessons_done", 0) or 0
    new_daily = current_daily + 1

    await user_repo.update(
        user.user_id,
        current_xp=user.current_xp + xp_earned,
        streak_days=new_streak,
        last_active_date=datetime.utcnow(),
        daily_lessons_done=new_daily,
    )

    lesson_repo = LessonRepository(session)
    await lesson_repo.complete(lesson_id, correct, xp_earned)

    # Topic / module advancement
    current_topic = getattr(user, "current_topic", 1)
    level_up_text = ""

    topic_done = await check_topic_complete(session, user.user_id, user.current_level, current_topic)
    if topic_done:
        vocab_repo = VocabularyRepository(session)
        max_topic = await vocab_repo.count_topics_in_level(user.current_level)
        if current_topic < max_topic:
            new_topic = current_topic + 1
            await user_repo.update(user.user_id, current_topic=new_topic)
            level_up_text += TOPIC_UP.format(topic=new_topic)
        elif user.current_level < MAX_LEVEL:
            new_level = user.current_level + 1
            from bot.services.gamification import LEVEL_TITLES as _LT
            title = _LT[new_level] if new_level < len(_LT) else f"Modul {new_level}"
            await user_repo.update(user.user_id, current_level=new_level, current_topic=1)
            level_up_text += MODULE_UP.format(module=new_level, module_title=title)
            level_up_text += LEVEL_UP.format(level=new_level, level_title=title)

    # Count referrals for achievement check
    from sqlalchemy import select, func as sqlfunc
    from bot.database.models import User as UserModel
    ref_count_r = await session.execute(
        select(sqlfunc.count(UserModel.user_id)).where(
            UserModel.referred_by == user.user_id
        )
    )
    referral_count = ref_count_r.scalar() or 0

    # Achievements
    mastered_total = await prog_repo.count_mastered(user.user_id)
    fresh = await user_repo.get(user.user_id)
    new_ach: list = []
    if fresh:
        new_ach = check_new_achievements(
            fresh, correct, total, mastered_total,
            referral_count=referral_count,
            daily_done=new_daily,
        )
        if new_ach:
            existing = set(filter(None, (fresh.achievements_earned or "").split(",")))
            existing.update(new_ach)
            await user_repo.update(user.user_id, achievements_earned=",".join(existing))

    await session.commit()

    # Restore shijoat pin with updated values
    if pin_id and chat_id:
        shijoat_pin_id = getattr(user, "shijoat_pin_id", None)
        if fresh and pin_id == shijoat_pin_id:
            try:
                pct = await _get_module_pct(session, fresh)
                await callback.bot.edit_message_text(
                    text=shijoat_pin_text(
                        fresh.shijoat_points,
                        fresh.current_level,
                        getattr(fresh, "current_topic", 1),
                        pct,
                        fresh.subscription_tier,
                    ),
                    chat_id=chat_id, message_id=pin_id,
                )
            except Exception:
                pass
        else:
            try:
                await callback.bot.delete_message(chat_id=chat_id, message_id=pin_id)
            except Exception:
                pass
            if fresh and getattr(fresh, "shijoat_pin_id", None):
                await _update_shijoat_pin(callback.bot, fresh, session)

    # Delete all lesson question messages
    if chat_id and msg_ids:
        await _try_delete(callback.bot, chat_id, msg_ids)

    await state.clear()

    summary = LESSON_COMPLETE.format(correct=correct, total=total, xp=xp_earned, streak=new_streak)
    praise = get_praise(correct, total, new_streak, streak_bonus)
    result_text = f"{summary}\n\n{praise}{level_up_text}"

    try:
        await callback.message.edit_text(result_text, reply_markup=lesson_result_kb())
    except Exception:
        await callback.message.answer(result_text, reply_markup=lesson_result_kb())

    # Send achievement pop-ups and broadcast
    for ach_key in new_ach:
        ach = ACHIEVEMENTS.get(ach_key)
        if ach:
            try:
                await callback.message.answer(ACHIEVEMENT_EARNED.format(name=ach["name"], desc=ach["desc"]))
            except Exception:
                pass

            # Broadcast achievement to all users after 2-second delay (background task)
            achiever_name = (fresh.full_name if fresh else None) or "Foydalanuvchi"
            from bot.database.base import async_session_maker
            asyncio.create_task(_broadcast_achievement(
                callback.bot,
                async_session_maker,
                user.user_id,
                achiever_name,
                ach_key,
                ach["name"],
                ach["desc"],
            ))

    await callback.answer()


# ── Congrat handler ───────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("congrat:"))
async def handle_congrat(callback: CallbackQuery, session: AsyncSession):
    parts = callback.data.split(":")
    if len(parts) < 3:
        await callback.answer("Xato ma'lumot", show_alert=True)
        return

    try:
        target_user_id = int(parts[1])
        ach_key = parts[2]
    except ValueError:
        await callback.answer("Xato ma'lumot", show_alert=True)
        return

    # Get sender name from DB
    repo = UserRepository(session)
    sender_user = await repo.get(callback.from_user.id)
    sender_name = (sender_user.full_name if sender_user else None) or "Kimdir"

    ach = ACHIEVEMENTS.get(ach_key)
    ach_name = ach["name"] if ach else ach_key

    # Send congrat to the achievement owner
    try:
        congrat_msg = await callback.bot.send_message(
            target_user_id,
            CONGRAT_SENT.format(sender_name=sender_name, ach_name=ach_name),
        )
        # Schedule auto-delete after 5 minutes
        asyncio.create_task(_delayed_delete(callback.bot, target_user_id, congrat_msg.message_id, delay=300))
    except Exception:
        pass

    # Show toast to clicker
    await callback.answer(CONGRAT_TOAST, show_alert=True)

    # Delete or edit the broadcast message that was clicked
    try:
        toast_msg = await callback.message.edit_reply_markup(reply_markup=None)
        if toast_msg:
            asyncio.create_task(_delayed_delete(callback.bot, callback.message.chat.id, callback.message.message_id, delay=300))
    except Exception:
        pass
