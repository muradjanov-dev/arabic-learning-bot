from datetime import datetime, date
from bot.database.models import User, SubscriptionTier
from bot.config import settings

LEVEL_XP_THRESHOLDS = [0, 200, 500, 900, 1400, 2000, 2700, 3500, 4400, 5400, 6500]
LEVEL_NAMES = [
    "", "Mubtadi (Yangi boshlovchi)", "Talib (Talabgor)", "Salik (Yo'lovchi)",
    "Arif (Bilimdon)", "Hafiz (Yodlovchi)", "Faqih (Mujtahid)",
    "Muhaddis (Hadisshunos)", "Mufassir (Tafsirchi)",
    "Alim (Olim)", "Hakim (Donishmand)"
]


def calculate_xp(correct: int, total: int, streak: int) -> tuple[int, int]:
    base = correct * settings.XP_PER_CORRECT
    lesson_bonus = settings.XP_LESSON_BONUS if correct >= total * 0.6 else 0
    streak_bonus = settings.STREAK_BONUS if streak >= 2 else 0
    total_xp = base + lesson_bonus + streak_bonus
    return total_xp, streak_bonus


def get_level_from_xp(xp: int) -> int:
    for lvl in range(len(LEVEL_XP_THRESHOLDS) - 1, 0, -1):
        if xp >= LEVEL_XP_THRESHOLDS[lvl]:
            return lvl
    return 1


def get_xp_for_next_level(xp: int) -> tuple[int, int]:
    level = get_level_from_xp(xp)
    if level >= len(LEVEL_XP_THRESHOLDS) - 1:
        return xp, 0
    current_threshold = LEVEL_XP_THRESHOLDS[level]
    next_threshold = LEVEL_XP_THRESHOLDS[level + 1]
    return current_threshold, next_threshold - current_threshold


def update_streak(user: User) -> tuple[int, bool]:
    today = date.today()
    last = user.last_active_date.date() if user.last_active_date else None
    is_new_day = last != today

    if not is_new_day:
        return user.streak_days, False

    if last is None or (today - last).days > 1:
        new_streak = 1
    else:
        new_streak = user.streak_days + 1

    return new_streak, True


def get_daily_shijoat(tier: SubscriptionTier) -> int:
    if tier == SubscriptionTier.UNLIMITED:
        return settings.UNLIMITED_SHIJOAT
    if tier == SubscriptionTier.PREMIUM:
        return settings.PREMIUM_DAILY_SHIJOAT
    return settings.FREE_DAILY_SHIJOAT


def tier_display(tier: SubscriptionTier) -> str:
    return {"free": "🆓 Bepul", "premium": "💎 Premium", "unlimited": "♾️ Unlimited"}.get(
        tier.value, "🆓 Bepul"
    )
