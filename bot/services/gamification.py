from datetime import date
from bot.database.models import User, SubscriptionTier
from bot.config import settings

LEVEL_XP_THRESHOLDS = [0, 200, 500, 900, 1400, 2000, 2700, 3500, 4400, 5400, 6500]

LEVEL_NAMES = [
    "",
    "Yangi boshlovchi 🌱",
    "Izlovchi 🔍",
    "O'rganuvchi 📖",
    "Bilimdon 💡",
    "Yodlovchi 🧠",
    "Mohir 🎯",
    "Ustoz ⭐",
    "Ekspert 🏅",
    "Professor 🎓",
    "Arab tili ustasi 👑",
]

LEVEL_TITLES = [
    "",
    "Alifbo (1) — ا ب ت ث ج ح خ + Birinchi so'zlar",
    "Alifbo (2) — د-ي barcha harflar + Lug'at",
    "Lug'at (1) — Maktab, Uy, Tabiat",
    "Grammatika — Harakatlar va Ta'rif ال",
    "Lug'at (2) — Ta'om, Transport, Shahar",
    "Muloqot — Salomlashish va Oila",
    "Grammatika — Olmosh, Savol, Ravish",
    "Sifatlar — Tavsif va His-tuyg'ular",
    "Fe'llar (1) — Harakat, Holat, Amr",
    "Fe'llar (2) — Predlog, Zarf, Muloqot",
]

TOPIC_NAMES = {
    # Module 1
    (1, 1): "Harflar: ا ب ت ث ج ح خ",
    (1, 2): "Birinchi so'zlar",
    (1, 3): "Jism a'zolari",
    (1, 4): "Ranglar",
    (1, 5): "Hayvonlar",
    (1, 6): "Raqamlar 1-7",
    # Module 2
    (2, 1): "Harflar: د ذ ر ز س ش ص",
    (2, 2): "Harflar: ض ط ظ ع غ ف ق",
    (2, 3): "Tabiat so'zlari",
    (2, 4): "Odamlar va narsalar",
    (2, 5): "Raqamlar 8-100",
    (2, 6): "Harflar: ك ل م ن و ه ي",
    (2, 7): "Maxsus harflar va hamzalar",
    # Module 3 — vocabulary only, no letters
    (3, 1): "Maktab so'zlari",
    (3, 2): "Uy so'zlari",
    (3, 3): "Tabiat va ob-havo",
    (3, 4): "Mevalar va sabzavotlar",
    (3, 5): "Kundalik narsalar",
    # Module 4
    (4, 1): "Harakatlar",
    (4, 2): "Ta'rif bilan so'zlar",
    (4, 3): "Muzakkar va Muannath",
    (4, 4): "Ikkilik shakli",
    (4, 5): "Ko'plik shakllari",
    # Module 5
    (5, 1): "Oddiy so'zlar",
    (5, 2): "Tabiat",
    (5, 3): "Ta'om va ichimlik",
    (5, 4): "Transport va yo'l",
    (5, 5): "Shahar va joylar",
    # Module 6
    (6, 1): "Salomlashish",
    (6, 2): "Oila",
    (6, 3): "Vaqt iboralari",
    (6, 4): "Bozor va xarid",
    (6, 5): "Sog'liq",
    # Module 7
    (7, 1): "Olmoshlar",
    (7, 2): "Savol so'zlari",
    (7, 3): "Millatlar",
    (7, 4): "Ravishlar",
    (7, 5): "Bog'lovchilar",
    # Module 8
    (8, 1): "Sifatlar",
    (8, 2): "Zid sifatlar",
    (8, 3): "Taqqoslash sifatlari",
    (8, 4): "His-tuyg'ular",
    (8, 5): "Muhim sifatlar",
    # Module 9
    (9, 1): "Fe'llar (harakatlar)",
    (9, 2): "Fe'llar (holat)",
    (9, 3): "Muzori' fe'llari",
    (9, 4): "Amr fe'llari",
    (9, 5): "Kundalik hayot fe'llari",
    # Module 10
    (10, 1): "Fe'llar (his-tuyg'u)",
    (10, 2): "Fe'llar (aqliy)",
    (10, 3): "Harf jarr (predloglar)",
    (10, 4): "Makonga oid zarflar",
    (10, 5): "Aloqa fe'llari 2",
}

ACHIEVEMENTS = {
    "first_lesson": {
        "name": "🎯 Birinchi qadam!",
        "desc": "Birinchi darsni muvaffaqiyatli yakunlash",
    },
    "streak_3": {
        "name": "🔥 Uch kunlik!",
        "desc": "Ketma-ket 3 kun dars qilish",
    },
    "streak_7": {
        "name": "⚡ Haftalik chempion!",
        "desc": "Ketma-ket 7 kun dars qilish",
    },
    "streak_14": {
        "name": "🔥 Ikki hafta!",
        "desc": "Ketma-ket 14 kun dars qilish",
    },
    "streak_30": {
        "name": "💫 Oylik qahramon!",
        "desc": "Ketma-ket 30 kun dars qilish",
    },
    "streak_60": {
        "name": "💫 Ikki oylik qahramon!",
        "desc": "Ketma-ket 60 kun dars qilish",
    },
    "words_10": {
        "name": "📚 10 so'z egasi!",
        "desc": "10 ta so'zni to'liq o'zlashtirish (mastery 4+)",
    },
    "words_25": {
        "name": "📖 25 so'z egasi!",
        "desc": "25 ta so'zni o'zlashtirish",
    },
    "words_50": {
        "name": "🏆 50 so'z ustasi!",
        "desc": "50 ta so'zni to'liq o'zlashtirish",
    },
    "words_100": {
        "name": "💎 100 so'z!",
        "desc": "100 ta so'zni to'liq o'zlashtirish",
    },
    "perfect": {
        "name": "💯 Mukammal dars!",
        "desc": "Bitta darsda barcha javoblarni to'g'ri berish",
    },
    "level_3": {
        "name": "🌟 3-daraja!",
        "desc": "3-darajaga ko'tarilish",
    },
    "level_5": {
        "name": "⭐ 5-daraja!",
        "desc": "5-darajaga ko'tarilish",
    },
    "level_10": {
        "name": "👑 Arab tili ustasi!",
        "desc": "10-darajaga ko'tarilish",
    },
    "module_5": {
        "name": "🚀 Yarim yo'l!",
        "desc": "5-modulga yetish",
    },
    "referral_1": {
        "name": "🤝 Birinchi do'st!",
        "desc": "1 do'stni taklif qilish",
    },
    "referral_5": {
        "name": "🌟 Do'stlar armiyasi!",
        "desc": "5 do'stni taklif qilish",
    },
    "daily_goal_1": {
        "name": "🎯 Kunlik maqsad!",
        "desc": "Bir kunda 3 ta dars bajarish",
    },
    "daily_goal_7": {
        "name": "📅 Haftalik intizom!",
        "desc": "7 kun ketma-ket kunlik maqsadni bajarish",
    },
    "speed_run": {
        "name": "⚡ Chaqmoq tezlik!",
        "desc": "Bir darsda barcha savollarni 30 soniyada javoblash",
    },
}


def check_new_achievements(
    user: User,
    correct: int,
    total: int,
    mastered_total: int,
    referral_count: int = 0,
    daily_done: int = 0,
) -> list[str]:
    """Returns list of newly earned achievement IDs."""
    earned = set(filter(None, (user.achievements_earned or "").split(",")))
    new_ones = []

    def _check(key: str):
        if key not in earned:
            new_ones.append(key)

    if total > 0:
        _check("first_lesson")
    if correct == total and total > 0:
        _check("perfect")
    if user.streak_days >= 3:
        _check("streak_3")
    if user.streak_days >= 7:
        _check("streak_7")
    if user.streak_days >= 14:
        _check("streak_14")
    if user.streak_days >= 30:
        _check("streak_30")
    if user.streak_days >= 60:
        _check("streak_60")
    if mastered_total >= 10:
        _check("words_10")
    if mastered_total >= 25:
        _check("words_25")
    if mastered_total >= 50:
        _check("words_50")
    if mastered_total >= 100:
        _check("words_100")
    if user.current_level >= 3:
        _check("level_3")
    if user.current_level >= 5:
        _check("level_5")
        _check("module_5")
    if user.current_level >= 10:
        _check("level_10")
    if referral_count >= 1:
        _check("referral_1")
    if referral_count >= 5:
        _check("referral_5")
    if daily_done >= 3:
        _check("daily_goal_1")

    return new_ones


def calculate_xp(correct: int, total: int, streak: int) -> tuple[int, int]:
    base = correct * settings.XP_PER_CORRECT
    lesson_bonus = settings.XP_LESSON_BONUS if correct >= total * 0.6 else 0
    streak_bonus = settings.STREAK_BONUS if streak >= 2 else 0
    return base + lesson_bonus + streak_bonus, streak_bonus


def get_level_from_xp(xp: int) -> int:
    for lvl in range(len(LEVEL_XP_THRESHOLDS) - 1, 0, -1):
        if xp >= LEVEL_XP_THRESHOLDS[lvl]:
            return lvl
    return 1


def get_xp_for_next_level(xp: int) -> tuple[int, int]:
    level = get_level_from_xp(xp)
    if level >= len(LEVEL_XP_THRESHOLDS) - 1:
        return xp, 0
    return LEVEL_XP_THRESHOLDS[level], LEVEL_XP_THRESHOLDS[level + 1] - LEVEL_XP_THRESHOLDS[level]


def update_streak(user: User) -> tuple[int, bool]:
    today = date.today()
    last = user.last_active_date.date() if user.last_active_date else None
    if last == today:
        return user.streak_days, False
    if last is None or (today - last).days > 1:
        return 1, True
    return user.streak_days + 1, True


def get_daily_shijoat(tier: SubscriptionTier) -> int:
    if tier == SubscriptionTier.UNLIMITED:
        return settings.UNLIMITED_SHIJOAT
    if tier == SubscriptionTier.PREMIUM:
        return settings.PREMIUM_DAILY_SHIJOAT
    return settings.FREE_DAILY_SHIJOAT


def tier_display(tier: SubscriptionTier) -> str:
    return {
        "free": "🆓 Bepul",
        "premium": "💎 Premium",
        "unlimited": "♾️ Cheksiz",
    }.get(tier.value, "🆓 Bepul")


def shijoat_pin_text(shijoat: int, module: int, topic: int, pct: int, tier: SubscriptionTier) -> str:
    tier_icon = {"free": "🆓", "premium": "💎", "unlimited": "♾️"}.get(tier.value, "🆓")
    bar_filled = int(pct / 100 * 6)
    bar = "🟩" * bar_filled + "⬜" * (6 - bar_filled)
    return (
        f"⚡ <b>Shijoat: {shijoat}</b>  ·  {tier_icon}\n"
        f"📊 {module}-modul T{topic}: {bar} {pct}%"
    )
