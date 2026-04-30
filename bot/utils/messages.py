WELCOME = (
    "Assalomu alaykum! 🌟\n\n"
    "Arab tili o'rganish safariga xush kelibsiz!\n"
    "Noodatiy uslubda — qiziqarli, oson va samarali!\n"
    "10 ta daraja, 500+ so'z, real talaffuz 🚀\n\n"
    "Avval bir-ikki savolga javob bering 😊"
)

ASK_NAME = "Ismingizni yozing — qanday chaqirishimni bilishim kerak 😊"
ASK_AGE = "Yoshingizni yozing (raqamda):"
ASK_ARABIC_LEVEL = "Arab tilini oldin o'rganganmisiz? Darajangizni tanlang:"

REGISTRATION_DONE = (
    "Zo'r! Hammasi tayyor — safar boshlanmoqda! 🎉\n\n"
    "Siz <b>{level}-darajadan</b> boshasiz.\n"
    "Har kuni 10 daqiqa — va natija ko'rasiz!\n\n"
    "Omad! 💪"
)

MAIN_MENU = "Asosiy menyu — qayerga ketamiz? 😊"

NO_SHIJOAT = (
    "Shijoatingiz tugadi! 😔\n\n"
    "Ertaga soat 00:01 da yangilanadi.\n"
    "Yoki Premium/Cheksiz obuna bilan to'xtovsiz o'rganing! 💎"
)

LESSON_START_CONFIRM = (
    "<b>✨ Yangi dars tayyorlanmoqda!</b>\n\n"
    "📦 Modul {module}  |  📚 Mavzu {topic}\n"
    "📝 {questions} ta savol\n"
    "⚡ {cost} Shijoat sarflanadi  |  💰 Sizda: <b>{shijoat}</b>\n"
    "📊 Mavzu: <b>{progress_pct}%</b> o'zlashtirilgan\n\n"
    "Tayyor bo'lsangiz — ketdik! 🚀"
)

LESSON_COMPLETE = (
    "<b>🎊 Dars yakunlandi!</b>\n\n"
    "✅ To'g'ri javoblar: <b>{correct}/{total}</b>\n"
    "⭐ Qozonilgan XP: <b>+{xp}</b>\n"
    "🔥 Streak: <b>{streak} kun</b>"
)

LEVEL_UP = (
    "\n\n🚀 <b>Yangi daraja ochildi!</b>\n"
    "Tabriklaymiz — siz endi <b>{level}-darajada!</b>\n"
    "<i>{level_title}</i>"
)

TOPIC_UP = (
    "\n\n🎯 <b>Mavzu yakunlandi!</b> 🎉\n"
    "Zo'r ish! Endi <b>Mavzu {topic}</b> ochildi.\n"
    "Yangi so'zlar, yangi imkoniyatlar — old'a! 💪"
)

MODULE_UP = (
    "\n\n🏆 <b>Modul yakunlandi!</b> 🎊\n"
    "Siz <b>{module}-modulni</b> muvaffaqiyatli tamomladingiz!\n"
    "<i>{module_title}</i>\n\n"
    "Yangi modul siz uchun ochildi. Davom eting! 🚀"
)

# Question templates
QUESTION_HEADER = "📝 Savol {idx}/{total}  |  ⚡ {shijoat}"
QUESTION_HEADER_NEW = "📝 Savol {idx}/{total}  |  ⚡ {shijoat}  |  🆕 YANGI SO'Z"
NEW_WORD_INTRO = "📚 <b>Yangi so'z:</b>\n<b>{arabic}</b> — {uzbek}\n"
QUESTION_VISUAL = "Quyidagi arabcha so'zning o'zbekcha ma'nosini toping:\n\n<b>{arabic}</b>"
QUESTION_AUDIO = "🔊 Audiони tinglang va to'g'ri tarjimani tanlang:"
QUESTION_JUMBLED = (
    "Quyidagi jumlani arabchaga tarjima qiling:\n\n"
    "<b>{uzbek}</b>\n\n"
    "👇 So'zlarni to'g'ri tartibda bosing:"
)

JUMBLED_SELECTED = "━━━━━━━━━━━━━━\n👉 <b>Javobingiz:</b>\n📝 <code>{words}</code>\n━━━━━━━━━━━━━━"
JUMBLED_EMPTY = "━━━━━━━━━━━━━━\n👉 <b>Javobingiz:</b>\n<i>(Quyidan so'zlarni tanlang)</i>\n━━━━━━━━━━━━━━"

CORRECT_MOTIVATIONS = [
    "Zo'r! 🎉", "Ajoyib! 🌟", "Bravo! 💪", "Mukammal! ✨",
    "Aniq javob! ⚡", "Olg'a! 🚀", "Yashang! 🏆", "Super! 🎊",
    "Siz uddalaysiz! 💎", "Ofarin! 👏", "Kuchli! 💥",
    "Daho! 🧠", "Zo'r odam! 🤩", "To'g'ri! ✅",
    "Cho'qqiga yaqinlashmoqdasiz! ⛰️", "Bilim — kuch! 📚",
    "Aql sinami! 🔥", "Ishonaman sizga! 🥇", "Iye-Iye qoyile! 🥇".
]

WRONG_HINTS = [
    "Bu safar emas. To'g'ri javob:",
    "Yo'q, esda saqlang:",
    "Yaqin keldingiz, lekin to'g'ri javob:",
    "Keyingi safar albatta! To'g'ri javob:",
]

SHIJOAT_PIN = (
    "⚡ <b>Shijoat: {shijoat}</b>\n"
    "{streak_str}  ·  {tier_icon}"
)

PROGRESS_PIN = "📊 <b>Dars</b>: {bar} {pct}%  ({current}/{total})"

PROFILE_TEXT = (
    "<b>👤 Mening sahifam</b>\n\n"
    "👤 Ism: <b>{name}</b>\n"
    "🎂 Yosh: {age}\n"
    "📚 Boshlang'ich daraja: {arabic_level}\n"
    "🏅 Kurs darajasi: <b>{level}/10</b>\n"
    "⭐ XP: {xp}\n"
    "🔥 Streak: <b>{streak} kun</b>\n"
    "⚡ Shijoat: <b>{shijoat}</b>\n"
    "💎 Obuna: {tier}\n"
    "🎯 O'zlashtirilgan so'zlar: <b>{mastered}</b>"
)

PROFILE_PROGRESS_HEADER = "\n\n<b>📊 Daraja bo'yicha bilim:</b>\n"
PROFILE_LEVEL_ROW = "{icon} <b>Daraja {n}</b> — {title}\n   {bar} {pct}% ({mastered}/{total} so'z)\n"
PROFILE_ACHIEVEMENTS_HEADER = "\n<b>🏆 Yutuqlar:</b>\n"

BANNED_MESSAGE = "Siz botdan blok qilindingiz. Admin bilan bog'laning."
SHIJOAT_UPSELL = "⚡ Shijoatingiz tugadi!\n\nPremium yoki Cheksiz obunaga o'tib, to'xtovsiz o'rganing! 💎"

SUBSCRIPTION_INFO = (
    "<b>Obuna turlari</b>\n\n"
    "🆓 <b>Bepul</b>: 100 Shijoat/kun\n\n"
    "💎 <b>Premium</b> — {premium_price}:\n"
    "• 1,000 Shijoat/kun\n"
    "• Barcha darslar ochiq\n\n"
    "♾️ <b>Cheksiz (deyarli)</b> — {unlimited_price}:\n"
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
    "yuboring. Admin tez orada tasdiqlaydi."
)

PAYMENT_RECEIPT_PROMPT = "To'lov cheki rasmini yuboring:\n\n(Bankdan screenshot yoki karta ko'chirmasi)"
PAYMENT_SENT = "Chekingiz adminga yuborildi! ✅\n\nTez orada tasdiqlanadi. Iltimos biroz kuting. 🙏"

PAYMENT_APPROVED = (
    "Tabriklaymiz! 🎉\n\n"
    "<b>{tier_name}</b> obunangiz faollashtirildi!\n"
    "📅 Muddati: <b>{expires}</b> gacha\n"
    "⚡ Shijoat: <b>{shijoat}/kun</b>\n\n"
    "Arab tili o'rganishda muvaffaqiyatlar tilaymiz! 💪🌟"
)

PAYMENT_DECLINED = (
    "Afsuski, to'lovingiz tasdiqlanmadi. ❌\n\n"
    "{reason}\n\n"
    "Qayta urinib ko'ring yoki admin bilan bog'laning."
)

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

TRIAL_NOTIFICATION = (
    "Salom, {name}! 🎁\n\n"
    "Arab tili o'rganish loyihasiga xush kelibsiz — siz uchun <b>2 kunlik Premium sinov</b> "
    "bepul berildi!\n\n"
    "⚡ Bugun <b>1,000 Shijoat</b> bilan dars qiling!\n"
    "📅 Sinov muddati: bugun va ertaga\n\n"
    "Arab tilini o'rganishda muvaffaqiyatlar tilaymiz! 💪🌟"
)

SUBSCRIPTION_EXPIRED = (
    "Sizning <b>{tier_name}</b> obunangiz tugadi. ⏰\n\n"
    "Endi kuniga 100 Shijoat bilan davom etamiz.\n\n"
    "Streak va natijalaringizni saqlab, obunani yangilashingiz mumkin! 🔥"
)

SUBSCRIPTION_EXPIRES_SOON = (
    "Sizning <b>{tier_name}</b> obunangiz <b>{days}</b> kunda tugaydi! ⏰\n\n"
    "Obunani yangilab, o'rganishni uzluksiz davom ettiring qadrligim. 💪"
)

REMINDER_MESSAGES = [
    "Arab tili sizni kutyapti! Bugungi shijoat ballaringizdan foydalaning! 🔥",
    "Atigi 5 daqiqa — va bugungi darsni yakunlaysiz. Streakni yo'qotmang! ⏳📚",
    "Bilim — boylik. Bugungi darsni o'tkazib yubormang! 📖✨",
    "Bugun dars qildingizmi? Streakni davom ettiring! 🔥📖",
    "Bilim yo'lida har kun bir qadam! Bugungi darsni boshlang. 💪",
]

ROADMAP_HEADER = "🗺 <b>O'quv yo'lxaritasi</b>\n\n"
ROADMAP_LEVEL_DONE = "✅ <b>{n}-daraja</b> — {title}\n   {bar} {pct}% o'zlashtirilgan\n\n"
ROADMAP_LEVEL_CURRENT = "🎯 <b>{n}-daraja</b> — {title}  ← Joriy\n   {bar} {pct}%\n\n"
ROADMAP_LEVEL_NEXT = "🔓 <b>{n}-daraja</b> — {title}\n   Ochiq (hali boshlanmagan)\n\n"
ROADMAP_LEVEL_LOCKED = "🔒 <b>{n}-daraja</b> — {title}\n   {prev}-darajani yakunlang\n\n"

ACHIEVEMENT_EARNED = "🏆 <b>Yangi yutuq!</b>\n\n{name}\n<i>{desc}</i>"

HOW_IT_WORKS = (
    "<b>🧠 Qanday ishlaydi?</b>\n\n"

    "<b>⚡ Shijoat (Stamina)</b>\n"
    "Har bir dars 10 Shijoat sarflaydi. Bepul: 100/kun, "
    "Premium: 1,000/kun, Cheksiz: 9,999/kun. "
    "Har kecha soat 00:01 da to'ldiriladi.\n\n"

    "<b>🔁 SRS algoritmi (Leitner)</b>\n"
    "Har so'zning o'zlashtirish darajasi 1-5. To'g'ri javob — "
    "keyingi takror uzoqroq (1→3→7→14→30 kun). "
    "Xato qilsangiz — daraja tushadi, 4 soatdan so'ng qayta keladi.\n\n"

    "<b>🏅 Kurs darajasi (1-10)</b>\n"
    "Ketma-ket 3 darsda 70%+ to'g'ri javob bersangiz — "
    "keyingi daraja avtomatik ochiladi.\n\n"

    "<b>🔥 Streak</b>\n"
    "Har kuni dars qilsangiz streak ortadi. "
    "2+ kun streakda +10 XP bonus. "
    "Bir kun o'tkazib yuborsangiz — streak noldan boshlanadi.\n\n"

    "<b>⭐ XP va unvonlar</b>\n"
    "Har to'g'ri javob +5 XP, dars yakunida +30 XP bonus. "
    "XP to'plash bilan unvon ko'tariladi "
    "(Yangi boshlovchi → Arab tili ustasi).\n\n"

    "<b>🏆 Yutuqlar</b>\n"
    "Birinchi dars, streak rekordlari, so'z milestones — "
    "har yutuqda maxsus nishon beriladi!"
)

ADMIN_MAIN = "<b>Admin Panel</b>\n\nXush kelibsiz, admin!"
ADMIN_STATS_HEADER = "<b>Bot Statistikasi</b>\n\n"
ADMIN_USER_LIST_HEADER = "<b>Foydalanuvchilar ro'yxati</b>\n\nJami: {total} ta\n\n"
ADMIN_USER_DETAIL = (
    "<b>Foydalanuvchi Ma'lumoti</b>\n\n"
    "🆔 ID: <code>{user_id}</code>\n"
    "👤 Ism: {name}\n"
    "🔗 Username: @{username}\n"
    "🎂 Yosh: {age}\n"
    "📚 Arab tili darajasi: {arabic_level}\n"
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
