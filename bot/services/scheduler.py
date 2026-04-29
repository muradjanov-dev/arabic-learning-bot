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
                )
                if user.shijoat_pin_id:
                    try:
                        text = shijoat_pin_text(new_shijoat, user.streak_days, user.subscription_tier)
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


def setup_scheduler(bot: Bot, session_factory: async_sessionmaker) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")

    # 00:01 — Shijoat reset
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

    # 19:00 — Daily reminders to inactive users
    scheduler.add_job(
        send_reminders,
        CronTrigger(hour=19, minute=0, timezone="Asia/Tashkent"),
        args=[session_factory, bot],
        id="daily_reminder",
        replace_existing=True,
    )

    return scheduler
