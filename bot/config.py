import os
from dotenv import load_dotenv

load_dotenv()


def _fix_db_url(url: str) -> str:
    # Strip whitespace/newlines that can creep in via env var injection
    url = url.strip().replace("\n", "").replace("\r", "")
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql://") and "+asyncpg" not in url:
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    DATABASE_URL: str = _fix_db_url(
        os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/arabic_bot")
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    ADMIN_IDS: list = list(map(int, os.getenv("ADMIN_IDS", "917456291").split(",")))
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
    WEBHOOK_PATH: str = "/webhook"
    WEB_SERVER_HOST: str = "0.0.0.0"
    WEB_SERVER_PORT: int = int(os.getenv("PORT", "8080"))

    # Shijoat economy
    FREE_DAILY_SHIJOAT: int = 100
    PREMIUM_DAILY_SHIJOAT: int = 1000
    UNLIMITED_SHIJOAT: int = 9999
    LESSON_SHIJOAT_COST: int = 10

    # XP
    XP_PER_CORRECT: int = 5
    XP_LESSON_BONUS: int = 30
    STREAK_BONUS: int = 10

    # Course settings
    MAX_COURSE_LEVEL: int = 10
    QUESTIONS_PER_LESSON: int = 15

    # Subscription pricing (2 weeks)
    PREMIUM_PRICE_SOM: int = 22_000
    UNLIMITED_PRICE_SOM: int = 49_000
    PREMIUM_PRICE_DISPLAY: str = "22,000 so'm (2 hafta)"
    UNLIMITED_PRICE_DISPLAY: str = "49,000 so'm (2 hafta)"
    SUBSCRIPTION_DAYS: int = 14

    # Trial
    TRIAL_DAYS: int = 2

    # Gemini AI (for content generation — one-time, cached in DB)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Payment card
    PAYMENT_CARD_NUMBER: str = "5614 6830 0539 3277"
    PAYMENT_CARD_HOLDER: str = "N. Murodjonov"


settings = Settings()
