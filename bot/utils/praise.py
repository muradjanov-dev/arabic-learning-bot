import random

PERFECT_PRAISE = [
    "🏆 Mukammal natija! Har bir so'z xotirangizga o'rnashib qoldi! 💎✨",
    "⭐ Ajoyib! To'liq to'g'ri javoblar — siz haqiqiy arab tili ustasisiz! 🌟",
    "🎊 Zo'r! 15/15 — bu zo'r natija! Davom eting! 🚀",
]

HIGH_PRAISE = [
    "🎉 Juda yaxshi natija! Har bir o'rgangan so'zingiz sizni bilim cho'qqisiga yaqinlashtirmoqda. Olg'a! 💪✨",
    "🌟 Yaxshi! Arab tili sirlarini ochavermoqdasiz, bugungi g'alaba kelajakdagi yutuqlaringiz poydevori! 🏅",
    "⚡ Ajoyib! Siz bu safarda davom etmoqdasiz! 📖💫",
]

MID_PRAISE = [
    "💪 Yaxshi harakat! Xatolar — o'rganishning bir qismi. Ertaga yanada yaxshiroq bo'lasiz! 🌱",
    "📚 Zo'r urinish! O'rta natija — lekin siz yanada ko'proqqa qodirSiz! Davom eting! 🔥",
    "🌙 Hammasi yaxshi! Arab tili sayohatingiz davom etmoqda. Har kun bir qadam oldinga! ✨",
]

LOW_PRAISE = [
    "🌱 Boshlash — o'ziyoq katta qadam! Ertaga yana urinib ko'ring, vaqt o'tishi bilan osonlashadi. 💫",
    "💙 Ruhingizni tushirmang! Har bir ulug' tilshunos shunday boshlagan. Sabr bilan o'rganing! 📖",
    "🤝 Bugun ozgina o'rgansangiz ham, ertaga ko'proq o'rganasiz! 🌟",
]

STREAK_BONUS = [
    "\n\n🔥 {streak} kunlik streak! Zo'r odat! +{bonus} qo'shimcha Olmos!",
    "\n\n⚡ {streak} kun uzluksiz! Kunlik streak bonusi: +{bonus} Olmos! Davom eting!",
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
