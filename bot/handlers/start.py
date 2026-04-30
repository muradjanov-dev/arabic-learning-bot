from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from bot.config import settings
from bot.database.models import ArabicLevel, UserProgress
from bot.database.repository import UserRepository, VocabularyRepository, ProgressRepository
from bot.keyboards.main_kb import (
    arabic_level_kb, back_to_menu_kb, roadmap_kb,
    confirm_lesson_kb, upsell_kb,
    reply_main_kb, KB_LESSON, KB_PROFILE, KB_ROADMAP, KB_LEADERBOARD,
    KB_PREMIUM, KB_SETTINGS, KB_REFERRAL,
)
from bot.services.gamification import shijoat_pin_text, tier_display, LEVEL_TITLES, get_level_from_xp, LEVEL_NAMES
from bot.services.lesson_service import TOTAL_PER_LESSON
from bot.utils.messages import (
    WELCOME, ASK_NAME, ASK_AGE, ASK_ARABIC_LEVEL, REGISTRATION_DONE, MAIN_MENU,
    SUBSCRIPTION_INFO, PROFILE_TEXT,
    LESSON_START_CONFIRM, NO_SHIJOAT,
    ROADMAP_HEADER, ROADMAP_LEVEL_DONE, ROADMAP_LEVEL_CURRENT,
    ROADMAP_LEVEL_NEXT, ROADMAP_LEVEL_LOCKED,
    REFERRAL_INFO, REFERRAL_RECEIVED, REFERRAL_SUCCESS,
)

router = Router()

MAX_LEVEL = 10
REFERRAL_SHIJOAT_BONUS = 500


class RegStates(StatesGroup):
    waiting_name = State()
    waiting_age = State()
    waiting_arabic_level = State()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _roadmap_bar(pct: int, width: int = 8) -> str:
    filled = int(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


async def _pin_shijoat(message: Message, user, session: AsyncSession) -> None:
    text = shijoat_pin_text(
        user.shijoat_points,
        user.current_level,
        getattr(user, "current_topic", 1),
        0,
        user.subscription_tier,
    )
    try:
        pin_msg = await message.answer(text)
        await message.bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=pin_msg.message_id,
            disable_notification=True,
        )
        repo = UserRepository(session)
        await repo.update(user.user_id, shijoat_pin_id=pin_msg.message_id)
        await session.commit()
    except Exception:
        pass


async def _get_bot_username(bot) -> str:
    try:
        me = await bot.get_me()
        return me.username or "arabicbot"
    except Exception:
        return "arabicbot"


async def _show_lesson_confirm(message: Message, user, session: AsyncSession) -> None:
    if user.shijoat_points < settings.LESSON_SHIJOAT_COST:
        await message.answer(NO_SHIJOAT, reply_markup=upsell_kb())
        return

    current_topic = getattr(user, "current_topic", 1)
    vocab_repo = VocabularyRepository(session)
    topic_words = await vocab_repo.get_words_for_topic(user.current_level, current_topic)
    total_in_topic = max(len(topic_words), 1)

    if topic_words:
        ids = [w.word_id for w in topic_words]
        r = await session.execute(
            select(func.count(UserProgress.id)).where(and_(
                UserProgress.user_id == user.user_id,
                UserProgress.word_id.in_(ids),
                UserProgress.mastery_level >= 3,
            ))
        )
        mastered_in_topic = r.scalar() or 0
    else:
        mastered_in_topic = 0

    progress_pct = int(mastered_in_topic / total_in_topic * 100)

    from bot.services.gamification import TOPIC_NAMES
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
    await message.answer(text, reply_markup=confirm_lesson_kb(user.shijoat_points))


async def _show_roadmap(message: Message, user, session: AsyncSession) -> None:
    prog_repo = ProgressRepository(session)
    level_progress = await prog_repo.get_progress_by_level(user.user_id)
    current = user.current_level

    text = ROADMAP_HEADER
    for n in range(1, MAX_LEVEL + 1):
        p = level_progress.get(n, {"total": 0, "seen": 0, "mastered": 0})
        total = p["total"] or 1
        pct = int(p["mastered"] / total * 100)
        title = LEVEL_TITLES[n] if n < len(LEVEL_TITLES) else f"Daraja {n}"
        bar = _roadmap_bar(pct)

        if n < current:
            text += ROADMAP_LEVEL_DONE.format(n=n, title=title, bar=bar, pct=pct)
        elif n == current:
            text += ROADMAP_LEVEL_CURRENT.format(n=n, title=title, bar=bar, pct=pct)
        elif n == current + 1:
            text += ROADMAP_LEVEL_NEXT.format(n=n, title=title)
        else:
            text += ROADMAP_LEVEL_LOCKED.format(n=n, title=title, prev=n - 1)

    await message.answer(text, reply_markup=roadmap_kb())


# ── /start ────────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, user, session: AsyncSession):
    await state.clear()

    # Extract referral code if present
    ref_user_id = None
    if message.text and len(message.text.split()) > 1:
        payload = message.text.split()[1]
        if payload.startswith("ref") and payload[3:].isdigit():
            ref_user_id = int(payload[3:])

    if user.is_registered:
        # Handle referral for already-registered user (ignore self-referral)
        if ref_user_id and ref_user_id != user.user_id and not getattr(user, "referred_by", None):
            await _process_referral(user, ref_user_id, session, message)

        await message.answer(MAIN_MENU, reply_markup=reply_main_kb())
        if not user.shijoat_pin_id:
            await _pin_shijoat(message, user, session)
        return

    # Store referral for after registration
    if ref_user_id and ref_user_id != user.user_id:
        await state.update_data(pending_referrer=ref_user_id)

    await message.answer(WELCOME, reply_markup=reply_main_kb())
    await message.answer(ASK_NAME)
    await state.set_state(RegStates.waiting_name)


async def _process_referral(new_user, referrer_id: int, session: AsyncSession, message) -> None:
    """Give both users +500 Shijoat for successful referral."""
    repo = UserRepository(session)
    referrer = await repo.get(referrer_id)
    if not referrer or not referrer.is_registered:
        return

    # Update new user: mark referred_by
    await repo.update(
        new_user.user_id,
        referred_by=referrer_id,
        shijoat_points=new_user.shijoat_points + REFERRAL_SHIJOAT_BONUS,
    )

    # Update referrer: give bonus
    await repo.update(
        referrer_id,
        shijoat_points=referrer.shijoat_points + REFERRAL_SHIJOAT_BONUS,
    )
    await session.commit()

    # Notify new user
    try:
        await message.answer(
            REFERRAL_RECEIVED.format(referrer_name=referrer.full_name or "Do'stingiz")
        )
    except Exception:
        pass

    # Notify referrer
    try:
        await message.bot.send_message(
            referrer_id,
            REFERRAL_SUCCESS.format(name=new_user.full_name or "Yangi foydalanuvchi"),
        )
    except Exception:
        pass


# ── Registration flow ─────────────────────────────────────────────────────────

@router.message(RegStates.waiting_name)
async def reg_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2 or len(name) > 60:
        await message.answer("Iltimos, to'g'ri ism kiriting (2–60 ta harf).")
        return
    await state.update_data(full_name=name)
    await message.answer(ASK_AGE)
    await state.set_state(RegStates.waiting_age)


@router.message(RegStates.waiting_age)
async def reg_age(message: Message, state: FSMContext):
    try:
        age = int(message.text.strip())
        if age < 5 or age > 100:
            raise ValueError
    except ValueError:
        await message.answer("Iltimos, to'g'ri yosh kiriting (5–100 oralig'ida raqam).")
        return
    await state.update_data(age=age)
    await message.answer(ASK_ARABIC_LEVEL, reply_markup=arabic_level_kb())
    await state.set_state(RegStates.waiting_arabic_level)


@router.callback_query(RegStates.waiting_arabic_level, F.data.startswith("reg_level:"))
async def reg_arabic_level(callback: CallbackQuery, state: FSMContext, user, session: AsyncSession):
    level_str = callback.data.split(":")[1]
    level_map = {
        "beginner": ArabicLevel.BEGINNER,
        "elementary": ArabicLevel.ELEMENTARY,
        "intermediate": ArabicLevel.INTERMEDIATE,
    }
    arabic_level = level_map.get(level_str, ArabicLevel.BEGINNER)
    start_level = {"beginner": 1, "elementary": 3, "intermediate": 6}.get(level_str, 1)

    data = await state.get_data()
    pending_referrer = data.get("pending_referrer")
    repo = UserRepository(session)
    await repo.update(
        user.user_id,
        full_name=data.get("full_name", ""),
        age=data.get("age"),
        arabic_level=arabic_level,
        current_level=start_level,
        is_registered=True,
    )
    await session.commit()
    await state.clear()

    full_name = data.get("full_name", "")
    await callback.message.edit_text(REGISTRATION_DONE.format(level=start_level, name=full_name))
    await callback.message.answer(MAIN_MENU, reply_markup=reply_main_kb())

    updated = await repo.get(user.user_id)
    if updated:
        await _pin_shijoat(callback.message, updated, session)

    # Process pending referral after registration
    if pending_referrer and pending_referrer != user.user_id:
        await _process_referral(updated or user, pending_referrer, session, callback.message)

    await callback.answer()


# ── Main menu inline nav ──────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:main")
async def menu_main(callback: CallbackQuery, state: FSMContext, user):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return
    await state.clear()
    await callback.message.edit_text(MAIN_MENU)
    await callback.answer()


# ── Referral handlers ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "referral:show")
async def referral_show(callback: CallbackQuery, user):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return
    bot_username = await _get_bot_username(callback.bot)
    link = f"https://t.me/{bot_username}?start=ref{user.user_id}"
    await callback.message.edit_text(
        REFERRAL_INFO.format(link=link),
        reply_markup=back_to_menu_kb(),
    )
    await callback.answer()


# ── Reply keyboard button handlers ───────────────────────────────────────────

@router.message(F.text == KB_LESSON)
async def kb_lesson(message: Message, state: FSMContext, user, session: AsyncSession):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    await state.clear()
    await _show_lesson_confirm(message, user, session)


@router.message(F.text == KB_PROFILE)
async def kb_profile(message: Message, user, session: AsyncSession):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return

    prog_repo = ProgressRepository(session)
    mastered = await prog_repo.count_mastered(user.user_id)
    xp_level = get_level_from_xp(user.current_xp)
    arabic_map = {"beginner": "Yangi boshlovchi", "elementary": "O'rta", "intermediate": "Ilg'or"}
    text = PROFILE_TEXT.format(
        name=user.full_name or "Noma'lum",
        age=user.age or "—",
        arabic_level=arabic_map.get(user.arabic_level.value, "—"),
        level=user.current_level,
        xp=f"{user.current_xp} ({LEVEL_NAMES[min(xp_level, 10)]})",
        streak=user.streak_days,
        shijoat=user.shijoat_points,
        tier=tier_display(user.subscription_tier),
        mastered=mastered,
    )
    await message.answer(text, reply_markup=back_to_menu_kb())


@router.message(F.text == KB_ROADMAP)
async def kb_roadmap(message: Message, user, session: AsyncSession):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    await _show_roadmap(message, user, session)


@router.message(F.text == KB_LEADERBOARD)
async def kb_leaderboard(message: Message, session: AsyncSession):
    from sqlalchemy import select
    from bot.database.models import User
    result = await session.execute(
        select(User).where(User.is_registered == True).order_by(User.current_xp.desc()).limit(10)
    )
    users = result.scalars().all()
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    lines = ["🏆 <b>Top 10 Reyting</b>\n"]
    for i, u in enumerate(users):
        name = u.full_name or "Noma'lum"
        lines.append(f"{medals[i]} {name} — {u.current_xp} 💎  🔥{u.streak_days}")
    await message.answer("\n".join(lines) if len(lines) > 1 else "Hozircha reyting yo'q.", reply_markup=back_to_menu_kb())


@router.message(F.text == KB_PREMIUM)
async def kb_premium(message: Message, user):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    from bot.keyboards.main_kb import subscription_kb
    text = SUBSCRIPTION_INFO.format(
        premium_price=settings.PREMIUM_PRICE_DISPLAY,
        unlimited_price=settings.UNLIMITED_PRICE_DISPLAY,
    )
    await message.answer(text, reply_markup=subscription_kb())


@router.message(F.text == KB_SETTINGS)
async def kb_settings(message: Message, user):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    from bot.keyboards.main_kb import settings_kb
    await message.answer("⚙️ <b>Sozlamalar</b>", reply_markup=settings_kb(user.is_notification_enabled))


@router.message(F.text == KB_REFERRAL)
async def kb_referral(message: Message, user):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    bot_username = await _get_bot_username(message.bot)
    link = f"https://t.me/{bot_username}?start=ref{user.user_id}"
    await message.answer(
        REFERRAL_INFO.format(link=link),
        reply_markup=back_to_menu_kb(),
    )


# ── Shortcut commands ─────────────────────────────────────────────────────────

@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext, user):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    await state.clear()
    await message.answer(MAIN_MENU, reply_markup=reply_main_kb())


@router.message(Command("lesson"))
async def cmd_lesson(message: Message, state: FSMContext, user, session: AsyncSession):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    await state.clear()
    await _show_lesson_confirm(message, user, session)


@router.message(Command("profile"))
async def cmd_profile(message: Message, user, session: AsyncSession):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    prog_repo = ProgressRepository(session)
    mastered = await prog_repo.count_mastered(user.user_id)
    xp_level = get_level_from_xp(user.current_xp)
    arabic_map = {"beginner": "Yangi boshlovchi", "elementary": "O'rta", "intermediate": "Ilg'or"}
    text = PROFILE_TEXT.format(
        name=user.full_name or "Noma'lum",
        age=user.age or "—",
        arabic_level=arabic_map.get(user.arabic_level.value, "—"),
        level=user.current_level,
        xp=f"{user.current_xp} ({LEVEL_NAMES[min(xp_level, 10)]})",
        streak=user.streak_days,
        shijoat=user.shijoat_points,
        tier=tier_display(user.subscription_tier),
        mastered=mastered,
    )
    await message.answer(text, reply_markup=back_to_menu_kb())


@router.message(Command("subscription"))
async def cmd_subscription(message: Message, user):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    from bot.keyboards.main_kb import subscription_kb
    text = SUBSCRIPTION_INFO.format(
        premium_price=settings.PREMIUM_PRICE_DISPLAY,
        unlimited_price=settings.UNLIMITED_PRICE_DISPLAY,
    )
    await message.answer(text, reply_markup=subscription_kb())
