import random
from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.repository import ProgressRepository, UserRepository
from bot.keyboards.main_kb import back_to_menu_kb, settings_kb, roadmap_kb, leaderboard_kb
from bot.services.gamification import (
    tier_display, LEVEL_NAMES, LEVEL_TITLES, ACHIEVEMENTS, get_level_from_xp, TOPIC_NAMES,
)
from bot.utils.messages import (
    PROFILE_TEXT, PROFILE_PROGRESS_HEADER, PROFILE_LEVEL_ROW,
    PROFILE_ACHIEVEMENTS_HEADER, HOW_IT_WORKS,
    ROADMAP_HEADER, ROADMAP_LEVEL_DONE, ROADMAP_LEVEL_CURRENT,
    ROADMAP_LEVEL_NEXT, ROADMAP_LEVEL_LOCKED,
    ROADMAP_TOPIC_ROW, ROADMAP_TOPIC_LOCKED,
    LEADERBOARD_HEADER, TUYAVOY_FACTS, DAILY_COMPARE,
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

    from sqlalchemy import select, and_, func as sqlfunc
    from bot.database.models import Vocabulary, UserProgress

    prog_repo = ProgressRepository(session)
    level_progress = await prog_repo.get_progress_by_level(user.user_id)

    text = ROADMAP_HEADER
    current = user.current_level
    current_topic = getattr(user, "current_topic", 1)

    for n in range(1, MAX_LEVEL + 1):
        p = level_progress.get(n, {"total": 0, "seen": 0, "mastered": 0})
        total = p["total"] or 1
        pct = int(p["mastered"] / total * 100)
        title = LEVEL_TITLES[n] if n < len(LEVEL_TITLES) else f"Daraja {n}"
        bar = _bar(pct)

        if n < current:
            text += ROADMAP_LEVEL_DONE.format(n=n, title=title, bar=bar, pct=pct)
        elif n == current:
            # Show level header
            text += ROADMAP_LEVEL_CURRENT.format(n=n, title=title, bar=bar, pct=pct)

            # Get all topics in this level
            result = await session.execute(
                select(sqlfunc.max(Vocabulary.topic_id)).where(
                    Vocabulary.level_id == n
                )
            )
            max_topic = result.scalar() or 1

            for t in range(1, max_topic + 1):
                topic_name = TOPIC_NAMES.get((n, t), f"Mavzu {t}")

                # Get mastery for this topic
                words_r = await session.execute(
                    select(Vocabulary.word_id).where(
                        and_(Vocabulary.level_id == n, Vocabulary.topic_id == t)
                    )
                )
                word_ids = [row[0] for row in words_r.fetchall()]
                if not word_ids:
                    continue

                mastered_r = await session.execute(
                    select(sqlfunc.count(UserProgress.id)).where(
                        and_(
                            UserProgress.user_id == user.user_id,
                            UserProgress.word_id.in_(word_ids),
                            UserProgress.mastery_level >= 3,
                        )
                    )
                )
                mastered_in_topic = mastered_r.scalar() or 0
                topic_pct = int(mastered_in_topic / len(word_ids) * 100)
                topic_bar = _bar(topic_pct, width=6)

                if t < current_topic:
                    icon = "✅"
                    marker = ""
                    text += ROADMAP_TOPIC_ROW.format(
                        icon=icon, n=t, name=topic_name,
                        bar=topic_bar, pct=topic_pct, marker=marker,
                    )
                elif t == current_topic:
                    icon = "🎯"
                    marker = "← Biz shu yerdamiz"
                    text += ROADMAP_TOPIC_ROW.format(
                        icon=icon, n=t, name=topic_name,
                        bar=topic_bar, pct=topic_pct, marker=marker,
                    )
                else:
                    text += ROADMAP_TOPIC_LOCKED.format(n=t, name=topic_name)

            text += "\n"
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

async def _build_leaderboard_text(session: AsyncSession, period: str = "weekly") -> str:
    from sqlalchemy import select, and_, func as sqlfunc
    from bot.database.models import User, Lesson

    period_labels = {
        "daily": "Kunlik",
        "weekly": "Haftalik",
        "monthly": "Oylik",
        "yearly": "Yillik",
    }
    label = period_labels.get(period, "Haftalik")

    now = datetime.utcnow()
    if period == "daily":
        since = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        since = now - timedelta(days=now.weekday())
        since = since.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "monthly":
        since = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == "yearly":
        since = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        since = now - timedelta(days=7)

    # Aggregate XP earned in period from lessons table
    result = await session.execute(
        select(
            Lesson.user_id,
            sqlfunc.sum(Lesson.xp_earned).label("period_xp"),
        )
        .where(
            and_(
                Lesson.is_completed == True,
                Lesson.completed_at >= since,
            )
        )
        .group_by(Lesson.user_id)
        .order_by(sqlfunc.sum(Lesson.xp_earned).desc())
        .limit(10)
    )
    rows = result.fetchall()

    if not rows:
        # Fall back to all-time XP
        result2 = await session.execute(
            select(User)
            .where(User.is_registered == True)
            .order_by(User.current_xp.desc())
            .limit(10)
        )
        users = result2.scalars().all()
        medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
        text = LEADERBOARD_HEADER.format(period=label)
        for i, u in enumerate(users):
            name = u.full_name or "Noma'lum"
            text += f"{medals[i]} {name} — {u.current_xp} 💎  🔥{u.streak_days}\n"
        text += f"\n{DAILY_COMPARE.format(fact=random.choice(TUYAVOY_FACTS))}"
        return text

    # Fetch user names for the user_ids
    user_ids = [r[0] for r in rows]
    users_result = await session.execute(
        select(User).where(User.user_id.in_(user_ids))
    )
    users_map = {u.user_id: u for u in users_result.scalars().all()}

    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    text = LEADERBOARD_HEADER.format(period=label)
    for i, (uid, xp) in enumerate(rows):
        u = users_map.get(uid)
        name = (u.full_name if u else None) or "Noma'lum"
        streak = u.streak_days if u else 0
        text += f"{medals[i]} {name} — {xp} 💎  🔥{streak}\n"

    text += f"\n{DAILY_COMPARE.format(fact=random.choice(TUYAVOY_FACTS))}"
    return text


@router.callback_query(F.data == "menu:leaderboard")
async def leaderboard_view(callback: CallbackQuery, session: AsyncSession):
    text = await _build_leaderboard_text(session, "weekly")
    await callback.message.edit_text(text, reply_markup=leaderboard_kb("weekly"))
    await callback.answer()


@router.callback_query(F.data.startswith("lb:"))
async def leaderboard_period(callback: CallbackQuery, session: AsyncSession):
    period = callback.data.split(":")[1]
    if period not in ("daily", "weekly", "monthly", "yearly"):
        await callback.answer("Noma'lum davr", show_alert=True)
        return
    text = await _build_leaderboard_text(session, period)
    await callback.message.edit_text(text, reply_markup=leaderboard_kb(period))
    await callback.answer()
