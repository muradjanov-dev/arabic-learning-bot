WELCOME = (
    "Assalomu alaykum! 🌟\n\n"
    "Arab tili o'rganish safariga xush kelibsiz!\n"
    "Bu safarda siz 10 darajali bilim cho'qqisiga ko'tariasiz.\n\n"
    "Avval ro'yxatdan o'tamiz..."
)

ASK_NAME = "Ismingizni kiriting:"

ASK_AGE = "Yoshingizni kiriting (raqamda):"

ASK_ARABIC_LEVEL = "Arab tili darajangizni tanlang:"

REGISTRATION_DONE = (
    "Ajoyib! Ro'yxatdan o'tish muvaffaqiyatli yakunlandi. 🎉\n\n"
    "Siz 1-darajadan boshlanasiz. Muvaffaqiyatlar!"
)

MAIN_MENU = "Asosiy menyu. Nima qilishni xohlaysiz?"

NO_SHIJOAT = (
    "Sizning shijoatingiz tugadi! 😔\n\n"
    "Ertaga yangi shijoat ballari yangilanadi.\n"
    "Yoki Premium obuna orqali cheksiz o'rganing! 💎"
)

LESSON_START_CONFIRM = (
    "<b>Bugungi dars</b>\n\n"
    "📝 {questions} ta savol\n"
    "⚡ {cost} Shijoat sarflanadi\n"
    "💰 Shijoatingiz: {shijoat}\n\n"
    "Boshlashga tayyormisiz?"
)

LESSON_COMPLETE = (
    "<b>Dars yakunlandi!</b>\n\n"
    "✅ To'g'ri javoblar: {correct}/{total}\n"
    "⭐ Earned XP: +{xp}\n"
    "🔥 Streak: {streak} kun"
)

QUESTION_VISUAL = "Quyidagi arabcha so'zning o'zbekcha tarjimasini toping:\n\n<b>{arabic}</b>"
QUESTION_AUDIO = "Audio eshiting va to'g'ri tarjimani tanlang:"
QUESTION_JUMBLED = (
    "Quyidagi jumlani arabchaga tarjima qiling:\n\n"
    "<b>{uzbek}</b>\n\n"
    "So'zlarni to'g'ri tartibda bosing:"
)
JUMBLED_SELECTED = "Tanlangan: {words}"
JUMBLED_EMPTY = "(hech narsa tanlanmagan)"

CORRECT_ANSWER = "✅ To'g'ri! +{xp} XP"
WRONG_ANSWER = "❌ Noto'g'ri! To'g'ri javob: <b>{correct}</b>"

PROFILE_TEXT = (
    "<b>Sahifam</b>\n\n"
    "👤 Ism: {name}\n"
    "🎂 Yosh: {age}\n"
    "📚 Boshlang'ich daraja: {arabic_level}\n"
    "🏅 Kurs darajasi: {level}/10\n"
    "⭐ XP: {xp}\n"
    "🔥 Streak: {streak} kun\n"
    "⚡ Shijoat: {shijoat}\n"
    "💎 Obuna: {tier}\n"
    "🎯 O'zlashtirilgan so'zlar: {mastered}"
)

BANNED_MESSAGE = "Siz botdan blok qilindingiz. Admin bilan bog'laning."

SHIJOAT_UPSELL = (
    "⚡ Shijoatingiz tugadi!\n\n"
    "Premium yoki Cheksiz obunaga o'tib, to'xtovsiz o'rganing! 💎"
)

# ── Subscription ──────────────────────────────────────────────────────────────

SUBSCRIPTION_INFO = (
    "<b>Obuna turlari</b>\n\n"
    "🆓 <b>Bepul</b>: 100 Shijoat/kun\n\n"
    "💎 <b>Premium</b> — {premium_price}:\n"
    "• 1,000 Shijoat/kun\n"
    "• Barcha darslar ochiq\n\n"
    "♾️ <b>Cheksiz</b> — {unlimited_price}:\n"
    "• 9,999 Shijoat/kun (deyarli cheksiz)\n"
    "• Barcha imkoniyatlar\n\n"
    "Quyidan tanlang:"
)

PAYMENT_INSTRUCTIONS = (
    "<b>{tier_name} Obuna</b>\n\n"
    "💰 Narxi: <b>{price}</b>\n\n"
    "To'lov qilish uchun:\n"
    "🏦 Karta raqami: <code>{card}</code>\n"
    "👤 Egasi: <b>{holder}</b>\n\n"
    "To'lovni amalga oshirgandan so'ng, to'lov chekini (screenshot yoki rasm) "
    "yuboring. Admin 24 soat ichida tasdiqlaydi."
)

PAYMENT_RECEIPT_PROMPT = (
    "To'lov cheki rasmini yuboring:\n\n"
    "(Bankdan screenshot yoki karta ko'chirmasi)"
)

PAYMENT_SENT = (
    "Chekingiz adminga yuborildi! ✅\n\n"
    "Tez orada tasdiqlanadi. Sabr qiling. 🙏"
)

PAYMENT_APPROVED = (
    "Tabriklaymiz! 🎉\n\n"
    "<b>{tier_name}</b> obunangiz faollashtirildi!\n"
    "📅 Muddati: <b>{expires}</b> gacha\n"
    "⚡ Shijoat: <b>{shijoat}/kun</b>\n\n"
    "Arab tili o'rganishda muvaffaqiyatlar! 💪🌟"
)

PAYMENT_DECLINED = (
    "Afsuski, to'lovingiz tasdiqlanmadi. ❌\n\n"
    "{reason}\n\n"
    "Qayta urinib ko'ring yoki admin bilan bog'laning."
)

# ── Admin payment notification ────────────────────────────────────────────────

ADMIN_PAYMENT_NOTIFICATION = (
    "💳 <b>Yangi to'lov so'rovi #{request_id}</b>\n\n"
    "👤 Foydalanuvchi: {name}\n"
    "🆔 ID: <code>{user_id}</code>\n"
    "🔗 Username: @{username}\n"
    "💎 Obuna turi: <b>{tier}</b>\n"
    "💰 Miqdor: <b>{amount:,} so'm</b>\n"
    "📅 Sana: {date}"
)

ADMIN_PAYMENT_APPROVED_MARK = "✅ TASDIQLANDI — {name} ({user_id})"
ADMIN_PAYMENT_DECLINED_MARK = "❌ RAD ETILDI — {name} ({user_id})"

# ── Trial ─────────────────────────────────────────────────────────────────────

TRIAL_NOTIFICATION = (
    "Assalomu alaykum, {name}! 🎁\n\n"
    "Siz botimizga kechagi keldingiz — <b>2 kunlik Premium sinov tarifi</b> "
    "sizga bepul berildi!\n\n"
    "⚡ Bugun <b>1,000 Shijoat</b> bilan dars qiling!\n"
    "📅 Sinov muddati: bugun va ertaga\n\n"
    "Arab tilini o'rganishni davom ettiring! 💪"
)

# ── Subscription expiry ───────────────────────────────────────────────────────

SUBSCRIPTION_EXPIRED = (
    "Sizning <b>{tier_name}</b> obunangiz tugadi. ⏰\n\n"
    "Endi kuniga 100 Shijoat bilan davom etasiz.\n\n"
    "O'rganishni to'xtatmang! Streak va natijalaringizni yo'qotmang — "
    "obunani yangilang va kuchingizdan to'liq foydalaning! 🔥"
)

SUBSCRIPTION_EXPIRES_SOON = (
    "Sizning <b>{tier_name}</b> obunangiz <b>{days}</b> kunda tugaydi! ⏰\n\n"
    "Obunani yangilab, o'rganishni uzluksiz davom ettiring. 💪"
)

# ── Admin panel ───────────────────────────────────────────────────────────────

ADMIN_MAIN = "<b>Admin Panel</b>\n\nXush kelibsiz, admin!"

ADMIN_STATS_HEADER = "<b>Bot Statistikasi</b>\n\n"

ADMIN_USER_LIST_HEADER = "<b>Foydalanuvchilar ro'yxati</b>\n\nJami: {total} ta\n\n"

ADMIN_USER_DETAIL = (
    "<b>Foydalanuvchi Ma'lumoti</b>\n\n"
    "🆔 ID: <code>{user_id}</code>\n"
    "👤 Ism: {name}\n"
    "🔗 Username: @{username}\n"
    "🎂 Yosh: {age}\n"
    "📚 Arab darajasi: {arabic_level}\n"
    "🏅 Kurs darajasi: {level}/10\n"
    "⭐ XP: {xp}\n"
    "🔥 Streak: {streak} kun\n"
    "⚡ Shijoat: {shijoat}\n"
    "💎 Obuna: {tier}\n"
    "📅 Qo'shilgan: {join_date}\n"
    "🕐 Oxirgi faollik: {last_active}\n"
    "🚫 Bloklangan: {is_banned}"
)

BROADCAST_ASK = "Barcha foydalanuvchilarga yuboriladigan xabarni kiriting:"
BROADCAST_CONFIRM = "Xabar {count} ta foydalanuvchiga yuboriladi. Davom etasizmi?"
BROADCAST_DONE = "Xabar {sent}/{total} foydalanuvchiga yuborildi."

REMINDER_MESSAGES = [
    "Sizning sergakligingiz qayerda qoldi? Arab tili sizni kutyapti! Bugungi shijoat ballaringizdan foydalaning! 🦉🔥",
    "Arab tilida yana bir jumlani o'rganishga atigi 5 daqiqa vaqtingiz ketadi. Kunlik seriyangizni (streak) yo'qotib qo'ymang! ⏳📚",
    "Har bir o'rgangan so'z jannatga bir qadam! Arab tilini o'rganishni davom ettiring. 🌙✨",
    "Bugun dars qildingizmi? Streak to'plamni davom ettiring! 🔥📖",
    "Bilim yo'lida har kun bir qadam! Bugungi darsni boshlang. 💪🕌",
]
