from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.repository import ProgressRepository, LessonRepository
from bot.keyboards.main_kb import back_to_menu_kb, settings_kb
from bot.database.repository import UserRepository
from bot.services.gamification import tier_display, LEVEL_NAMES, get_level_from_xp
from bot.utils.messages import PROFILE_TEXT, MAIN_MENU

router = Router()


@router.callback_query(F.data == "menu:profile")
async def profile_view(callback: CallbackQuery, user, session: AsyncSession):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return

    prog_repo = ProgressRepository(session)
    mastered = await prog_repo.count_mastered(user.user_id)

    arabic_level_map = {"beginner": "Yangi boshlovchi", "elementary": "O'rta daraja", "intermediate": "Ilg'or"}
    xp_level = get_level_from_xp(user.current_xp)

    text = PROFILE_TEXT.format(
        name=user.full_name or "Noma'lum",
        age=user.age or "—",
        arabic_level=arabic_level_map.get(user.arabic_level.value, "—"),
        level=user.current_level,
        xp=f"{user.current_xp} ({LEVEL_NAMES[min(xp_level, 10)]})",
        streak=user.streak_days,
        shijoat=user.shijoat_points,
        tier=tier_display(user.subscription_tier),
        mastered=mastered,
    )
    await callback.message.edit_text(text, reply_markup=back_to_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "menu:settings")
async def settings_view(callback: CallbackQuery, user):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return
    await callback.message.edit_text(
        "Sozlamalar:",
        reply_markup=settings_kb(user.is_notification_enabled),
    )
    await callback.answer()


@router.callback_query(F.data == "settings:toggle_notif")
async def toggle_notifications(callback: CallbackQuery, user, session: AsyncSession):
    repo = UserRepository(session)
    new_val = not user.is_notification_enabled
    await repo.update(user.user_id, is_notification_enabled=new_val)
    status = "yoqildi ✅" if new_val else "o'chirildi ❌"
    await callback.answer(f"Bildirishnomalar {status}")

    # Refresh user object for keyboard
    updated = await repo.get(user.user_id)
    await callback.message.edit_reply_markup(reply_markup=settings_kb(updated.is_notification_enabled))


@router.callback_query(F.data == "menu:leaderboard")
async def leaderboard_view(callback: CallbackQuery, session: AsyncSession):
    from sqlalchemy import select, func
    from bot.database.models import User
    result = await session.execute(
        select(User).where(User.is_registered == True).order_by(User.current_xp.desc()).limit(10)
    )
    users = result.scalars().all()

    if not users:
        await callback.message.edit_text("Hozircha reyting ma'lumotlari yo'q.", reply_markup=__import__("bot.keyboards.main_kb", fromlist=["back_to_menu_kb"]).back_to_menu_kb())
        await callback.answer()
        return

    from bot.keyboards.main_kb import back_to_menu_kb as btm
    lines = ["🏆 <b>Top 10 Reyting</b>\n"]
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    for i, u in enumerate(users):
        name = u.full_name or "Noma'lum"
        lines.append(f"{medals[i]} {name} — {u.current_xp} XP")

    await callback.message.edit_text("\n".join(lines), reply_markup=btm())
    await callback.answer()
