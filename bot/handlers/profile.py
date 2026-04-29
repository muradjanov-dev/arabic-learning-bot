from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.repository import ProgressRepository, UserRepository
from bot.keyboards.main_kb import back_to_menu_kb, settings_kb, roadmap_kb
from bot.services.gamification import (
    tier_display, LEVEL_NAMES, LEVEL_TITLES, ACHIEVEMENTS, get_level_from_xp,
)
from bot.utils.messages import (
    PROFILE_TEXT, PROFILE_PROGRESS_HEADER, PROFILE_LEVEL_ROW,
    PROFILE_ACHIEVEMENTS_HEADER, HOW_IT_WORKS,
    ROADMAP_HEADER, ROADMAP_LEVEL_DONE, ROADMAP_LEVEL_CURRENT,
    ROADMAP_LEVEL_NEXT, ROADMAP_LEVEL_LOCKED,
)

router = Router()

MAX_LEVEL = 10


def _bar(pct: int, width: int = 8) -> str:
    filled = int(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


# ── Profile ───────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:profile")
async def profile_view(callback: CallbackQuery, user, session: AsyncSession):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return

    prog_repo = ProgressRepository(session)
    mastered = await prog_repo.count_mastered(user.user_id)

    arabic_level_map = {
        "beginner": "Yangi boshlovchi",
        "elementary": "O'rta daraja",
        "intermediate": "Ilg'or",
    }
    xp_level = get_level_from_xp(user.current_xp)

    text = PROFILE_TEXT.format(
        name=user.full_name or "Noma'lum",
        age=user.age or "—",
        arabic_level=arabic_level_map.get(user.arabic_level.value, "—"),
        level=user.current_level,
        xp=f"{user.current_xp} ({LEVEL_NAMES[min(xp_level, MAX_LEVEL)]})",
        streak=user.streak_days,
        shijoat=user.shijoat_points,
        tier=tier_display(user.subscription_tier),
        mastered=mastered,
    )

    # Per-level progress breakdown
    level_progress = await prog_repo.get_progress_by_level(user.user_id)
    text += PROFILE_PROGRESS_HEADER
    for n in range(1, MAX_LEVEL + 1):
        p = level_progress.get(n, {"total": 0, "seen": 0, "mastered": 0})
        total = p["total"] or 1
        mst = p["mastered"]
        pct = int(mst / total * 100)

        if n < user.current_level:
            icon = "✅"
        elif n == user.current_level:
            icon = "🎯"
        else:
            icon = "🔒"

        title = LEVEL_TITLES[n] if n < len(LEVEL_TITLES) else f"Daraja {n}"
        text += PROFILE_LEVEL_ROW.format(
            icon=icon, n=n, title=title,
            bar=_bar(pct), pct=pct, mastered=mst, total=p["total"],
        )

    # Achievements
    earned = set(filter(None, (user.achievements_earned or "").split(",")))
    if earned:
        text += PROFILE_ACHIEVEMENTS_HEADER
        for key, ach in ACHIEVEMENTS.items():
            if key in earned:
                text += f"  ✅ {ach['name']}\n"

    await callback.message.edit_text(text, reply_markup=back_to_menu_kb())
    await callback.answer()


# ── Roadmap ───────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:roadmap")
async def roadmap_view(callback: CallbackQuery, user, session: AsyncSession):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return

    prog_repo = ProgressRepository(session)
    level_progress = await prog_repo.get_progress_by_level(user.user_id)

    text = ROADMAP_HEADER
    current = user.current_level

    for n in range(1, MAX_LEVEL + 1):
        p = level_progress.get(n, {"total": 0, "seen": 0, "mastered": 0})
        total = p["total"] or 1
        pct = int(p["mastered"] / total * 100)
        title = LEVEL_TITLES[n] if n < len(LEVEL_TITLES) else f"Daraja {n}"
        bar = _bar(pct)

        if n < current:
            text += ROADMAP_LEVEL_DONE.format(n=n, title=title, bar=bar, pct=pct)
        elif n == current:
            text += ROADMAP_LEVEL_CURRENT.format(n=n, title=title, bar=bar, pct=pct)
        elif n == current + 1:
            text += ROADMAP_LEVEL_NEXT.format(n=n, title=title)
        else:
            text += ROADMAP_LEVEL_LOCKED.format(n=n, title=title, prev=n - 1)

    await callback.message.edit_text(text, reply_markup=roadmap_kb())
    await callback.answer()


# ── Settings ──────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:settings")
async def settings_view(callback: CallbackQuery, user):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return
    await callback.message.edit_text(
        "⚙️ <b>Sozlamalar</b>",
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
    updated = await repo.get(user.user_id)
    await callback.message.edit_reply_markup(reply_markup=settings_kb(updated.is_notification_enabled))


@router.callback_query(F.data == "settings:how_it_works")
async def how_it_works(callback: CallbackQuery):
    await callback.message.edit_text(HOW_IT_WORKS, reply_markup=back_to_menu_kb())
    await callback.answer()


# ── Leaderboard ───────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:leaderboard")
async def leaderboard_view(callback: CallbackQuery, session: AsyncSession):
    from sqlalchemy import select
    from bot.database.models import User

    result = await session.execute(
        select(User)
        .where(User.is_registered == True)
        .order_by(User.current_xp.desc())
        .limit(10)
    )
    users = result.scalars().all()

    if not users:
        await callback.message.edit_text("Hozircha reyting ma'lumotlari yo'q.", reply_markup=back_to_menu_kb())
        await callback.answer()
        return

    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    lines = ["🏆 <b>Top 10 Reyting</b>\n"]
    for i, u in enumerate(users):
        name = u.full_name or "Noma'lum"
        lines.append(f"{medals[i]} {name} — {u.current_xp} XP  🔥{u.streak_days}")

    await callback.message.edit_text("\n".join(lines), reply_markup=back_to_menu_kb())
    await callback.answer()
