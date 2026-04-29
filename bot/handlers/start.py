from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.database.models import ArabicLevel
from bot.database.repository import UserRepository
from bot.keyboards.main_kb import (
    main_menu_kb, arabic_level_kb, back_to_menu_kb,
    reply_main_kb, KB_LESSON, KB_PROFILE, KB_ROADMAP, KB_LEADERBOARD,
    KB_PREMIUM, KB_SETTINGS,
)
from bot.services.gamification import shijoat_pin_text, tier_display
from bot.utils.messages import (
    WELCOME, ASK_NAME, ASK_AGE, ASK_ARABIC_LEVEL, REGISTRATION_DONE, MAIN_MENU,
    SUBSCRIPTION_INFO, PROFILE_TEXT,
)

router = Router()


class RegStates(StatesGroup):
    waiting_name = State()
    waiting_age = State()
    waiting_arabic_level = State()


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _pin_shijoat(message: Message, user, session: AsyncSession) -> None:
    """Send and pin the shijoat status message; store its ID in the user row."""
    text = shijoat_pin_text(user.shijoat_points, user.streak_days, user.subscription_tier)
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


# ── /start ────────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, user, session: AsyncSession):
    await state.clear()
    if user.is_registered:
        await message.answer(MAIN_MENU, reply_markup=reply_main_kb())
        await message.answer("👇", reply_markup=main_menu_kb())
        # Re-pin shijoat if missing
        if not user.shijoat_pin_id:
            await _pin_shijoat(message, user, session)
        return

    await message.answer(WELCOME, reply_markup=reply_main_kb())
    await message.answer(ASK_NAME)
    await state.set_state(RegStates.waiting_name)


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

    await callback.message.edit_text(REGISTRATION_DONE.format(level=start_level))
    await callback.message.answer(MAIN_MENU, reply_markup=reply_main_kb())
    await callback.message.answer("👇", reply_markup=main_menu_kb())

    # Refresh user to get updated data, then pin shijoat
    updated = await repo.get(user.user_id)
    if updated:
        await _pin_shijoat(callback.message, updated, session)
    await callback.answer()


# ── Main menu inline nav ──────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:main")
async def menu_main(callback: CallbackQuery, state: FSMContext, user):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return
    await state.clear()
    await callback.message.edit_text(MAIN_MENU, reply_markup=main_menu_kb())
    await callback.answer()


# ── Reply keyboard button handlers ───────────────────────────────────────────

@router.message(F.text == KB_LESSON)
async def kb_lesson(message: Message, state: FSMContext, user):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    await state.clear()
    await message.answer("📖 Dars boshlash:", reply_markup=main_menu_kb())


@router.message(F.text == KB_PROFILE)
async def kb_profile(message: Message, user, session: AsyncSession):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    from bot.database.repository import ProgressRepository
    from bot.services.gamification import LEVEL_TITLES, ACHIEVEMENTS, get_level_from_xp
    from bot.utils.messages import PROFILE_TEXT

    prog_repo = ProgressRepository(session)
    mastered = await prog_repo.count_mastered(user.user_id)
    xp_level = get_level_from_xp(user.current_xp)
    from bot.services.gamification import LEVEL_NAMES
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
    # Trigger the inline roadmap view by sending an inline menu
    await message.answer(MAIN_MENU, reply_markup=main_menu_kb())


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
        lines.append(f"{medals[i]} {name} — {u.current_xp} XP  🔥{u.streak_days}")
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


# ── Shortcut commands ─────────────────────────────────────────────────────────

@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext, user):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    await state.clear()
    await message.answer(MAIN_MENU, reply_markup=reply_main_kb())
    await message.answer("👇", reply_markup=main_menu_kb())


@router.message(Command("lesson"))
async def cmd_lesson(message: Message, state: FSMContext, user):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    await state.clear()
    await message.answer("📖 Dars boshlash:", reply_markup=main_menu_kb())


@router.message(Command("profile"))
async def cmd_profile(message: Message, user):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    await message.answer(MAIN_MENU, reply_markup=main_menu_kb())


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
