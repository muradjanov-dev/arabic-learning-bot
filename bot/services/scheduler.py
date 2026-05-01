import logging
import random
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import async_sessionmaker
from aiogram import Bot

from bot.config import settings
from bot.database.repository import UserRepository, PaymentRepository
from bot.database.models import SubscriptionTier
from bot.services.gamification import get_daily_shijoat, shijoat_pin_text
from bot.utils.messages import (
    REMINDER_MESSAGES, TRIAL_NOTIFICATION,
    SUBSCRIPTION_EXPIRED, SUBSCRIPTION_EXPIRES_SOON,
    DAILY_GOAL_PROGRESS, DAILY_GOAL_DONE,
    LEADERBOARD_HEADER, TUYAVOY_FACTS,
)
from bot.keyboards.main_kb import renew_subscription_kb, main_menu_kb

logger = logging.getLogger(__name__)

TIER_NAMES = {
    SubscriptionTier.PREMIUM: "💎 Premium",
    SubscriptionTier.UNLIMITED: "♾️ Cheksiz",
}


async def reset_shijoat(session_factory: async_sessionmaker, bot: Bot) -> None:
    logger.info("Running daily Shijoat reset...")
    async with session_factory() as session:
        try:
            repo = UserRepository(session)
            users = await repo.get_all_registered()
            for user in users:
                new_shijoat = get_daily_shijoat(user.subscription_tier)
                await repo.update(
                    user.user_id,
                    shijoat_points=new_shijoat,
                    last_shijoat_reset=datetime.utcnow(),
                    daily_lessons_done=0,
                    last_daily_reset=datetime.utcnow(),
                )
                if user.shijoat_pin_id:
                    try:
                        from sqlalchemy import select, and_, func as sqlfunc
                        from bot.database.repository import VocabularyRepository
                        from bot.database.models import UserProgress
                        current_topic = getattr(user, "current_topic", 1)
                        vocab_repo = VocabularyRepository(session)
                        words = await vocab_repo.get_words_for_topic(user.current_level, current_topic)
                        pct = 0
                        if words:
                            ids = [w.word_id for w in words]
                            r = await session.execute(
                                select(sqlfunc.count(UserProgress.id)).where(and_(
                                    UserProgress.user_id == user.user_id,
                                    UserProgress.word_id.in_(ids),
                                    UserProgress.mastery_level >= 3,
                                ))
                            )
                            pct = int((r.scalar() or 0) / len(words) * 100)
                        text = shijoat_pin_text(
                            new_shijoat, user.current_level, current_topic, pct, user.subscription_tier
                        )
                        await bot.edit_message_text(
                            text=text,
                            chat_id=user.user_id,
                            message_id=user.shijoat_pin_id,
                        )
                    except Exception:
                        pass
            await session.commit()
            logger.info(f"Shijoat reset for {len(users)} users.")
        except Exception as e:
            await session.rollback()
            logger.error(f"Shijoat reset failed: {e}")


async def check_expired_subscriptions(session_factory: async_sessionmaker, bot: Bot) -> None:
    """Downgrade expired premium/unlimited users and notify them."""
    logger.info("Checking expired subscriptions...")
    async with session_factory() as session:
        try:
            pay_repo = PaymentRepository(session)
            expired_users = await pay_repo.get_users_with_expired_subscriptions()
            user_repo = UserRepository(session)

            for user in expired_users:
                tier_name = TIER_NAMES.get(user.subscription_tier, "Obuna")
                await user_repo.update(
                    user.user_id,
                    subscription_tier=SubscriptionTier.FREE,
                    subscription_expires=None,
                    shijoat_points=settings.FREE_DAILY_SHIJOAT,
                )
                try:
                    await bot.send_message(
                        user.user_id,
                        SUBSCRIPTION_EXPIRED.format(tier_name=tier_name),
                        reply_markup=renew_subscription_kb(),
                    )
                except Exception:
                    pass

            if expired_users:
                await session.commit()
                logger.info(f"Downgraded {len(expired_users)} expired subscriptions.")
        except Exception as e:
            await session.rollback()
            logger.error(f"Subscription expiry check failed: {e}")


async def notify_expiring_soon(session_factory: async_sessionmaker, bot: Bot) -> None:
    """Warn users whose subscription expires in exactly 2 days."""
    async with session_factory() as session:
        try:
            from sqlalchemy import select, and_
            from bot.database.models import User

            target_start = datetime.utcnow() + timedelta(days=2)
            target_end = target_start.replace(hour=23, minute=59, second=59)
            target_start = target_start.replace(hour=0, minute=0, second=0)

            result = await session.execute(
                select(User).where(
                    and_(
                        User.subscription_expires >= target_start,
                        User.subscription_expires <= target_end,
                        User.subscription_tier != SubscriptionTier.FREE,
                        User.is_registered == True,
                        User.is_banned == False,
                    )
                )
            )
            users = result.scalars().all()

            for user in users:
                tier_name = TIER_NAMES.get(user.subscription_tier, "Obuna")
                try:
                    await bot.send_message(
                        user.user_id,
                        SUBSCRIPTION_EXPIRES_SOON.format(tier_name=tier_name, days=2),
                        reply_markup=renew_subscription_kb(),
                    )
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Expiry-soon check failed: {e}")


async def give_trials(session_factory: async_sessionmaker, bot: Bot) -> None:
    """Give 2-day premium trial to users who registered yesterday."""
    logger.info("Checking trial eligibility...")
    async with session_factory() as session:
        try:
            pay_repo = PaymentRepository(session)
            trial_users = await pay_repo.get_users_for_trial()
            user_repo = UserRepository(session)
            expires = datetime.utcnow() + timedelta(days=settings.TRIAL_DAYS)

            for user in trial_users:
                await user_repo.update(
                    user.user_id,
                    subscription_tier=SubscriptionTier.PREMIUM,
                    subscription_expires=expires,
                    shijoat_points=settings.PREMIUM_DAILY_SHIJOAT,
                    trial_given=True,
                )
                try:
                    await bot.send_message(
                        user.user_id,
                        TRIAL_NOTIFICATION.format(name=user.full_name or "Do'stim"),
                        reply_markup=main_menu_kb(),
                    )
                except Exception:
                    pass

            if trial_users:
                await session.commit()
                logger.info(f"Trial given to {len(trial_users)} users.")
        except Exception as e:
            await session.rollback()
            logger.error(f"Trial give failed: {e}")


async def send_reminders(session_factory: async_sessionmaker, bot: Bot) -> None:
    logger.info("Sending daily reminders...")
    async with session_factory() as session:
        try:
            repo = UserRepository(session)
            users = await repo.get_users_for_notification()
            sent = 0
            for user in users:
                try:
                    await bot.send_message(user.user_id, random.choice(REMINDER_MESSAGES))
                    sent += 1
                except Exception:
                    pass
            logger.info(f"Reminders sent to {sent}/{len(users)} users.")
        except Exception as e:
            logger.error(f"Reminder send failed: {e}")


async def send_daily_goal_reminder(session_factory: async_sessionmaker, bot: Bot) -> None:
    """At 15:00 — remind users who haven't completed 3 lessons yet."""
    logger.info("Sending daily goal reminders...")
    async with session_factory() as session:
        try:
            from sqlalchemy import select
            from bot.database.models import User

            result = await session.execute(
                select(User).where(
                    User.is_registered == True,
                    User.is_banned == False,
                    User.is_notification_enabled == True,
                    User.daily_lessons_done < 3,
                )
            )
            users = result.scalars().all()

            progress_msgs = {
                0: ("😴", "Hali birorta dars qilmadingiz. Boshlash vaqti!"),
                1: ("💪", "Zo'r start! Yana 2 ta dars qoldi."),
                2: ("🔥", "Deyarli yetib keldingiz! Yana 1 ta dars qoldi."),
            }

            sent = 0
            for user in users:
                done = getattr(user, "daily_lessons_done", 0) or 0
                emoji, msg = progress_msgs.get(done, ("📚", "Darsni davom ettiring!"))
                try:
                    await bot.send_message(
                        user.user_id,
                        DAILY_GOAL_PROGRESS.format(done=done, emoji=emoji, msg=msg),
                    )
                    sent += 1
                except Exception:
                    pass
            logger.info(f"Daily goal reminders sent to {sent}/{len(users)} users.")
        except Exception as e:
            logger.error(f"Daily goal reminder failed: {e}")


async def send_evening_encouragement(session_factory: async_sessionmaker, bot: Bot) -> None:
    """At 20:00 — congratulate users who completed 3+ lessons today."""
    logger.info("Sending evening encouragement...")
    async with session_factory() as session:
        try:
            from sqlalchemy import select
            from bot.database.models import User

            result = await session.execute(
                select(User).where(
                    User.is_registered == True,
                    User.is_banned == False,
                    User.is_notification_enabled == True,
                    User.daily_lessons_done >= 3,
                )
            )
            users = result.scalars().all()

            sent = 0
            for user in users:
                try:
                    await bot.send_message(user.user_id, DAILY_GOAL_DONE)
                    sent += 1
                except Exception:
                    pass
            logger.info(f"Evening encouragement sent to {sent}/{len(users)} users.")
        except Exception as e:
            logger.error(f"Evening encouragement failed: {e}")


async def _send_period_leaderboard(
    session_factory: async_sessionmaker,
    bot: Bot,
    period: str,
    period_label: str,
    since: datetime,
) -> None:
    """Broadcast period leaderboard to all users."""
    from sqlalchemy import select, and_, func as sqlfunc
    from bot.database.models import User, Lesson

    async with session_factory() as session:
        try:
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
                return

            user_ids = [r[0] for r in rows]
            users_result = await session.execute(
                select(User).where(User.user_id.in_(user_ids))
            )
            users_map = {u.user_id: u for u in users_result.scalars().all()}

            medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
            text = LEADERBOARD_HEADER.format(period=period_label)
            for i, (uid, xp) in enumerate(rows):
                u = users_map.get(uid)
                name = (u.full_name if u else None) or "Noma'lum"
                streak = u.streak_days if u else 0
                text += f"{medals[i]} {name} — {xp} 💎  🔥{streak}\n"

            # Send to all registered users
            all_users_result = await session.execute(
                select(User).where(
                    User.is_registered == True,
                    User.is_banned == False,
                    User.is_notification_enabled == True,
                )
            )
            all_users = all_users_result.scalars().all()

            # Use congrat_kb for top user if available
            top_uid = rows[0][0] if rows else None
            top_user = users_map.get(top_uid)
            kb = None
            if top_user:
                # No specific achievement key for leaderboard, just use a simple kb
                from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"🎊 {top_user.full_name or 'G`olibni'} tabrikladim!",
                        callback_data=f"congrat:{top_uid}:leaderboard_{period}",
                    )]
                ])

            for u in all_users:
                try:
                    await bot.send_message(u.user_id, text, reply_markup=kb)
                except Exception:
                    pass

            logger.info(f"{period_label} leaderboard broadcast sent to {len(all_users)} users.")
        except Exception as e:
            logger.error(f"Period leaderboard broadcast failed: {e}")


async def send_progress_comparison(session_factory: async_sessionmaker, bot: Bot) -> None:
    """Tue & Fri — tell each user what % of all users they're ahead of."""
    logger.info("Sending progress comparison notifications...")
    async with session_factory() as session:
        try:
            from sqlalchemy import select
            from bot.database.models import User

            result = await session.execute(
                select(User).where(
                    User.is_registered == True,
                    User.is_banned == False,
                    User.is_notification_enabled == True,
                )
            )
            users = result.scalars().all()
            if len(users) < 2:
                return

            total = len(users)
            all_xp = sorted(u.current_xp for u in users)

            sent = 0
            for user in users:
                lower = sum(1 for xp in all_xp if xp < user.current_xp)
                percentile = int(lower / total * 100)
                if percentile < 10:
                    continue  # skip bottom 10% — don't demotivate

                fact = random.choice(TUYAVOY_FACTS)
                msg = (
                    f"🐪 Tuyavoy: Siz hozir barcha o'quvchilarning "
                    f"<b>{percentile}%</b> dan oldingizda! 🏆\n\n"
                    f"💡 {fact}"
                )
                try:
                    await bot.send_message(user.user_id, msg)
                    sent += 1
                except Exception:
                    pass

            logger.info(f"Progress comparison sent to {sent}/{total} users.")
        except Exception as e:
            logger.error(f"Progress comparison failed: {e}")


async def send_daily_leaderboard(session_factory: async_sessionmaker, bot: Bot) -> None:
    """23:55 — daily top 10 leaderboard."""
    now = datetime.utcnow()
    since = now.replace(hour=0, minute=0, second=0, microsecond=0)
    await _send_period_leaderboard(session_factory, bot, "daily", "Kunlik", since)


async def send_weekly_leaderboard(session_factory: async_sessionmaker, bot: Bot) -> None:
    """Sunday 23:55 — weekly top 10 leaderboard."""
    now = datetime.utcnow()
    since = now - timedelta(days=now.weekday())
    since = since.replace(hour=0, minute=0, second=0, microsecond=0)
    await _send_period_leaderboard(session_factory, bot, "weekly", "Haftalik", since)


async def send_monthly_leaderboard(session_factory: async_sessionmaker, bot: Bot) -> None:
    """Last day of month 23:55 — monthly top 10 leaderboard."""
    now = datetime.utcnow()
    since = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    await _send_period_leaderboard(session_factory, bot, "monthly", "Oylik", since)


def setup_scheduler(bot: Bot, session_factory: async_sessionmaker) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")

    # 00:01 — Shijoat reset + daily_lessons_done reset
    scheduler.add_job(
        reset_shijoat,
        CronTrigger(hour=0, minute=1, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="shijoat_reset",
        replace_existing=True,
    )

    # 00:05 — Give 2-day trial to yesterday's registrants
    scheduler.add_job(
        give_trials,
        CronTrigger(hour=0, minute=5, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="give_trials",
        replace_existing=True,
    )

    # 08:00 — Check expired subscriptions & downgrade
    scheduler.add_job(
        check_expired_subscriptions,
        CronTrigger(hour=8, minute=0, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="expiry_check",
        replace_existing=True,
    )

    # 08:05 — Warn users expiring in 2 days
    scheduler.add_job(
        notify_expiring_soon,
        CronTrigger(hour=8, minute=5, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="expiry_soon",
        replace_existing=True,
    )

    # 15:00 — Daily goal reminder (for users with < 3 lessons done)
    scheduler.add_job(
        send_daily_goal_reminder,
        CronTrigger(hour=15, minute=0, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="daily_goal_reminder",
        replace_existing=True,
    )

    # 19:00 — Daily reminders to inactive users
    scheduler.add_job(
        send_reminders,
        CronTrigger(hour=19, minute=0, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="daily_reminder",
        replace_existing=True,
    )

    # 20:00 — Evening encouragement for users who completed 3+ lessons
    scheduler.add_job(
        send_evening_encouragement,
        CronTrigger(hour=20, minute=0, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="evening_encouragement",
        replace_existing=True,
    )

    # Tue & Fri 18:00 — "you're ahead of X% of users"
    scheduler.add_job(
        send_progress_comparison,
        CronTrigger(day_of_week="tue,fri", hour=18, minute=0, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="progress_comparison",
        replace_existing=True,
    )

    # 23:55 — Daily leaderboard broadcast
    scheduler.add_job(
        send_daily_leaderboard,
        CronTrigger(hour=23, minute=55, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="daily_leaderboard",
        replace_existing=True,
    )

    # Sunday 23:55 — Weekly leaderboard broadcast
    scheduler.add_job(
        send_weekly_leaderboard,
        CronTrigger(day_of_week="sun", hour=23, minute=55, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="weekly_leaderboard",
        replace_existing=True,
    )

    # Last day of month 23:55 — Monthly leaderboard broadcast
    scheduler.add_job(
        send_monthly_leaderboard,
        CronTrigger(day="last", hour=23, minute=55, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="monthly_leaderboard",
        replace_existing=True,
    )

    return scheduler
