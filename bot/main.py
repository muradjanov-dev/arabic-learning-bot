import asyncio
import logging
import os
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.config import settings
from bot.database.base import engine, async_session_maker
from bot.database.models import Base
from bot.middlewares.db_session import DbSessionMiddleware
from bot.middlewares.user_check import UserCheckMiddleware
from bot.handlers import start, lesson, profile, admin, subscription
from bot.services.scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _get_storage():
    # Only use Redis if REDIS_URL points to a real Redis service
    # (not the default localhost which won't exist on Railway)
    redis_url = (settings.REDIS_URL or "").strip()
    if not redis_url or "localhost" in redis_url or "127.0.0.1" in redis_url:
        logger.info("Using MemoryStorage for FSM (no Redis configured)")
        return MemoryStorage()
    try:
        from aiogram.fsm.storage.redis import RedisStorage
        storage = RedisStorage.from_url(redis_url)
        logger.info(f"Using Redis FSM storage at {redis_url.split('@')[-1]}")
        return storage
    except Exception as e:
        logger.warning(f"Redis init failed ({e}), falling back to MemoryStorage")
        return MemoryStorage()


async def _notify_admins_startup(bot: Bot) -> None:
    """Send a deployment notification to all admins after startup."""
    deploy_id = os.getenv("RAILWAY_DEPLOYMENT_ID", "local")[:8]
    commit = os.getenv("RAILWAY_GIT_COMMIT_SHA", "unknown")[:7]
    env = os.getenv("RAILWAY_ENVIRONMENT_NAME", "local")
    mode = "Webhook" if settings.WEBHOOK_URL else "Polling"
    text = (
        "🚀 <b>Bot ishga tushdi!</b>\n\n"
        f"🕐 Vaqt: <code>{datetime.utcnow().strftime('%d.%m.%Y %H:%M')} UTC</code>\n"
        f"🌿 Muhit: <code>{env}</code>\n"
        f"📦 Deploy: <code>{deploy_id}</code>\n"
        f"🔖 Commit: <code>{commit}</code>\n"
        f"🔄 Rejim: <code>{mode}</code>\n\n"
        "Yangilanish muvaffaqiyatli o'rnatildi. ✅"
    )
    for admin_id in settings.ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            logger.warning(f"Could not notify admin {admin_id} of startup: {e}")


async def _auto_seed_vocabulary() -> None:
    """Populate vocabulary; wipe and re-seed if old/religious/single-topic data detected."""
    from sqlalchemy import select, func, delete
    from bot.database.models import Vocabulary
    from scripts.seed_data import VOCABULARY, RELIGIOUS_CATEGORIES, RELIGIOUS_WORDS

    async with async_session_maker() as session:
        count = (await session.execute(select(func.count(Vocabulary.word_id)))).scalar() or 0
        if count > 0:
            sample = (await session.execute(select(Vocabulary).limit(20))).scalars().all()
            has_religious = any(
                (w.category in RELIGIOUS_CATEGORIES or w.arabic_word in RELIGIOUS_WORDS)
                for w in sample
            )
            max_topic = (await session.execute(
                select(func.max(Vocabulary.topic_id))
            )).scalar() or 1
            if has_religious or max_topic <= 1 or count < len(VOCABULARY):
                reason = (
                    "religious content" if has_religious
                    else "no topic differentiation" if max_topic <= 1
                    else f"word count mismatch ({count} vs {len(VOCABULARY)})"
                )
                await session.execute(delete(Vocabulary))
                await session.commit()
                logger.info(f"Wiped old vocabulary ({reason}) — re-seeding.")
            else:
                logger.info(f"Vocabulary already populated ({count} words, max topic={max_topic}).")
                return
        for item in VOCABULARY:
            session.add(Vocabulary(**item))
        await session.commit()
        logger.info(f"Auto-seeded {len(VOCABULARY)} vocabulary words.")


async def _run_column_migrations() -> None:
    from sqlalchemy import text
    migrations = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS achievements_earned TEXT DEFAULT ''",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS shijoat_pin_id INTEGER",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS current_topic INTEGER NOT NULL DEFAULT 1",
        "ALTER TABLE vocabulary ADD COLUMN IF NOT EXISTS topic_id INTEGER NOT NULL DEFAULT 1",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS referred_by INTEGER",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS daily_lessons_done INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_daily_reset TIMESTAMP",
    ]
    async with engine.begin() as conn:
        for sql in migrations:
            await conn.execute(text(sql))
    logger.info("Column migrations applied.")


async def on_startup(bot: Bot) -> None:
    # Retry DB connection — cold-start of Postgres can take a few seconds
    last_err = None
    for attempt in range(1, 11):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info(f"Database tables ensured (attempt {attempt}).")
            break
        except Exception as e:
            last_err = e
            logger.warning(f"DB connect attempt {attempt}/10 failed: {type(e).__name__}: {e}")
            await asyncio.sleep(min(attempt * 2, 10))
    else:
        logger.error(f"Database unreachable after 10 attempts. Last error: {last_err}")
        raise last_err

    try:
        await _run_column_migrations()
    except Exception as e:
        logger.warning(f"Column migrations skipped: {e}")

    try:
        await _auto_seed_vocabulary()
    except Exception as e:
        logger.error(f"Auto-seed failed: {e}")

    # Register bot commands visible in Telegram menu
    from aiogram.types import BotCommand
    await bot.set_my_commands([
        BotCommand(command="start", description="Bosh menyu"),
        BotCommand(command="profile", description="Mening sahifam"),
        BotCommand(command="lesson", description="Dars boshlash"),
        BotCommand(command="subscription", description="Obuna va Premium"),
    ])

    if settings.WEBHOOK_URL:
        webhook_url = f"{settings.WEBHOOK_URL.rstrip('/')}{settings.WEBHOOK_PATH}"
        await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
        logger.info(f"Webhook set: {webhook_url}")

    # Notify admins about successful (re)deployment
    await _notify_admins_startup(bot)


async def on_shutdown(bot: Bot) -> None:
    if settings.WEBHOOK_URL:
        await bot.delete_webhook()
    await engine.dispose()
    logger.info("Bot shutdown.")


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=_get_storage())

    dp.message.middleware(DbSessionMiddleware(async_session_maker))
    dp.callback_query.middleware(DbSessionMiddleware(async_session_maker))
    dp.message.middleware(UserCheckMiddleware())
    dp.callback_query.middleware(UserCheckMiddleware())

    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(lesson.router)
    dp.include_router(profile.router)
    dp.include_router(subscription.router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return dp


async def main() -> None:
    if not settings.BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set. Check your environment variables.")

    # Surface DB host so misconfigured DATABASE_URL is obvious in logs
    import re
    host_match = re.search(r"@([^/]+)/", settings.DATABASE_URL or "")
    db_host = host_match.group(1) if host_match else "unknown"
    logger.info(f"DATABASE host: {db_host}")
    if "localhost" in db_host or "127.0.0.1" in db_host:
        logger.error(
            "DATABASE_URL points to localhost — on Railway this won't work. "
            "Set DATABASE_URL=${{Postgres.DATABASE_URL}} in service variables."
        )

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = build_dispatcher()

    scheduler = setup_scheduler(bot, async_session_maker)
    scheduler.start()
    logger.info("Scheduler started.")

    try:
        if settings.WEBHOOK_URL:
            app = web.Application()
            handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
            handler.register(app, path=settings.WEBHOOK_PATH)
            setup_application(app, dp, bot=bot)

            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, settings.WEB_SERVER_HOST, settings.WEB_SERVER_PORT)
            await site.start()
            logger.info(f"Webhook server on {settings.WEB_SERVER_HOST}:{settings.WEB_SERVER_PORT}")
            await asyncio.Event().wait()
        else:
            logger.info("Starting polling...")
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
