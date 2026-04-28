import random

PERFECT_PRAISE = [
    "🎉 Masha'Allah! Mukammal natija! Har bir so'z sizning qalbingizga o'rnashib qoldi! 💎✨",
    "🏆 SubhanAllah! 15/15 — siz haqiqiy arab tili ustasisiz! Davom eting, ilm zinapoyasida! 🌟",
    "⭐ Alloh rahmat bersin! To'liq to'g'ri javoblar! Siz faxrlanishga loyiqsiz! 🎊",
]

HIGH_PRAISE = [
    "🎉 Masha'Allah! Siz bu darsni ajoyib yakunladingiz! Har bir o'rgangan so'zingiz sizni ilm cho'qqisiga yaqinlashtirmoqda. Olga qadam bosishdan to'xtamang! 💪✨",
    "🌟 Barakalloh! Juda yaxshi natija! Arab tili sirlarini ochavermasiz, bugungi g'alaba kelajakdagi yutuqlaringiz poydevori! 🏅",
    "⚡ Ajoyib! Siz bu safarda davom etmoqdasiz! Har bir dars sizni Qur'on tiliga yaqinlashtiradi! 📖💫",
]

MID_PRAISE = [
    "💪 Yaxshi harakat! Xatolar — o'rganishning bir qismi. Ertaga yanada yaxshiroq bo'lasiz! 🌱",
    "📚 Zo'r! O'rta natija — lekin siz yanada ko'proqqa qodirSiz! Davom eting, shijoat bilan! 🔥",
    "🌙 Hammasi yaxshi! Arab tili sayohatingiz davom etmoqda. Har kun bir qadam oldinga! ✨",
]

LOW_PRAISE = [
    "🌱 Boshlash — o'ziyoq katta qadam! Ertaga yana urinib ko'ring, vaqt o'tishi bilan osonlashadi. 💫",
    "💙 Ruhingizni tushirmang! Har bir ulug' olim shunday boshlagan. Sabr va iztiror bilan o'rganing! 📖",
    "🤲 Alloh o'rganishingizni osonlashtirsin! Bugun az o'rgansangiz ham, ertaga ko'proq o'rganasiz! 🌟",
]

STREAK_BONUS = [
    "\n\n🔥 {streak} kunlik streak! Siz ajoyib odatni shakllantirmoqdasiz! +{bonus} qo'shimcha XP!",
    "\n\n⚡ {streak} kun uzluksiz! Kunlik streak bonusi: +{bonus} XP! Davom eting!",
]


def get_praise(correct: int, total: int, streak: int = 0, streak_bonus: int = 0) -> str:
    ratio = correct / total if total > 0 else 0

    if ratio == 1.0:
        text = random.choice(PERFECT_PRAISE)
    elif ratio >= 0.8:
        text = random.choice(HIGH_PRAISE)
    elif ratio >= 0.5:
        text = random.choice(MID_PRAISE)
    else:
        text = random.choice(LOW_PRAISE)

    if streak >= 2 and streak_bonus > 0:
        text += random.choice(STREAK_BONUS).format(streak=streak, bonus=streak_bonus)

    return text
