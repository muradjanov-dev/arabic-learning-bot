WELCOME = (
    "Assalomu alaykum! 🌟\n\n"
    "🐪 <b>Tuyavoy</b>: Salom do'stim! Men Tuyavoy — arab tili cho'llarini biladigon zavqli tuya!\n"
    "Men seni arabcha so'zlar olamiga olib kiraman — qiziqarli, oson va samarali usulda!\n"
    "10 ta daraja, 500+ so'z, real talaffuz bor bu safarda 🚀\n"
    "Do'stlaringni ham taklif qilsang — ikkalang ham 500 Shijoat olasiz! 🎁\n\n"
    "Avval bir-ikki savolga javob bering 😊"
)

ASK_NAME = "🐪 Tuyavoy: Mening ismim Tuyavoy... sening isming nima? Yozib yubor! 😊"
ASK_AGE = "🐪 Tuyavoy: Yoshingizni yozing (raqamda) — yoshga qarab darsni moslashtiramiz:"
ASK_ARABIC_LEVEL = "🐪 Tuyavoy: Arab tilini oldin o'rganganmisiz? Darajangizni tanlang:"

REGISTRATION_DONE = (
    "🐪 Tuyavoy: Zo'r, {name}! Hammasi tayyor — safar boshlanmoqda! 🎉\n\n"
    "Siz <b>{level}-darajadan</b> boshlaysiz.\n"
    "Har kuni 10 daqiqa — va natija ko'rasiz!\n\n"
    "Omad! 💪 Tuyavoy siz bilan birga! 🐪"
)

MAIN_MENU = "🐪 Tuyavoy: Qayerga ketamiz? 😊"

NO_SHIJOAT = (
    "🐪 Tuyavoy: Voy, Shijoatingiz tugabdi! 😔\n\n"
    "Lekin xafa bo'lmang — do'stingizni taklif qiling va ikkalangiz ham 500 Shijoat olasiz! 🎁\n\n"
    "Yoki Premium/Cheksiz obuna bilan to'xtovsiz o'rganing! 💎\n\n"
    "Ertaga soat 00:01 da Shijoat yangilanadi."
)

LESSON_START_CONFIRM = (
    "<b>✨ Yangi dars tayyorlanmoqda!</b>\n\n"
    "📦 Modul {module}  |  📚 Mavzu {topic}: <i>{topic_name}</i>\n\n"
    "📝 {questions} ta savol\n"
    "⚡ {cost} Shijoat sarflanadi  |  💰 Sizda: <b>{shijoat}</b>\n"
    "📊 Mavzu: <b>{module_pct}%</b> o'zlashtirilgan\n\n"
    "🐪 Tuyavoy: Tayyor bo'lsangiz — ketdik! 🚀"
)

LESSON_COMPLETE = (
    "<b>🎊 Dars yakunlandi!</b>\n\n"
    "✅ To'g'ri javoblar: <b>{correct}/{total}</b>\n"
    "💎 Qozonilgan Olmos: <b>+{xp}</b>\n"
    "🔥 Streak: <b>{streak} kun</b>\n\n"
    "🐪 Tuyavoy: Ajoyib ish! Davom eting, cho'l yo'li oldinda! 🏜️"
)

LEVEL_UP = (
    "\n\n🚀 <b>Yangi daraja ochildi!</b>\n"
    "🐪 Tuyavoy: Voy, zo'r! Siz endi <b>{level}-darajada!</b>\n"
    "<i>{level_title}</i>"
)

TOPIC_UP = (
    "\n\n🎯 <b>Mavzu yakunlandi!</b> 🎉\n"
    "🐪 Tuyavoy: Yangi mavzuga yetib keldik! Endi <b>Mavzu {topic}</b> boshlanmoqda.\n"
    "Yangi so'zlar, yangi imkoniyatlar — olg'a! 💪"
)

MODULE_UP = (
    "\n\n🏆 <b>Modul yakunlandi!</b> 🎊\n"
    "🐪 Tuyavoy: Qoyilmaqom! <b>{module}-modulni</b> tamomladingiz!\n"
    "<i>{module_title}</i>\n\n"
    "Yangi modul siz uchun ochildi. Davom eting! 🚀"
)

# Question templates
QUESTION_HEADER = "📝 Savol {idx}/{total}  |  ⚡ {shijoat}"
QUESTION_HEADER_NEW = "📝 Savol {idx}/{total}  |  ⚡ {shijoat}  |  🆕 YANGI SO'Z"
NEW_WORD_INTRO = "📚 <b>Yangi so'z:</b>\n<b>{arabic}</b> — {uzbek}\n"
QUESTION_VISUAL = "Quyidagi arabcha so'zning o'zbekcha ma'nosini toping:\n\n<b>{arabic}</b>"
QUESTION_AUDIO = "🔊 Audioni tinglang va to'g'ri tarjimani tanlang:"
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
    "Aql sinami! 🔥", "Ishonaman sizga! 🥇", "Iye-Iye qoyile! 🥇",
    "🐪 Tuyavoy ham xursand! 🎊", "Shunday davom eting! 🌟",
    "Arabcha egallayapsiz! 🏅", "Fantastik! 🦁", "Barakalla! 🌙",
    "Mana shu! ✊", "Tengsiz! 👑", "Yangi rekord! 📈",
    "So'z yodlab qoldingiz! 🧠", "Tuyavoy sizga qoyil! 🐪",
    "Arab tili ustasi bo'lyapsiz! 🎓",
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
    "💎 Olmos: {xp}\n"
    "🔥 Streak: <b>{streak} kun</b>\n"
    "⚡ Shijoat: <b>{shijoat}</b>\n"
    "💎 Obuna: {tier}\n"
    "🎯 O'zlashtirilgan so'zlar: <b>{mastered}</b>"
)

PROFILE_PROGRESS_HEADER = "\n\n<b>📊 Daraja bo'yicha bilim:</b>\n"
PROFILE_LEVEL_ROW = "{icon} <b>Daraja {n}</b> — {title}\n   {bar} {pct}% ({mastered}/{total} so'z)\n"
PROFILE_ACHIEVEMENTS_HEADER = "\n<b>🏆 Yutuqlar:</b>\n"

BANNED_MESSAGE = "Siz botdan blok qilindingiz. Admin bilan bog'laning."
SHIJOAT_UPSELL = "⚡ Shijoatingiz tugadi!\n\n🐪 Tuyavoy: Do'stingizni taklif qiling — 500 Shijoat oling! Yoki Premium/Cheksiz obunaga o'tib, to'xtovsiz o'rganing! 💎"

SUBSCRIPTION_INFO = (
    "<b>Obuna turlari</b>\n\n"
    "🆓 <b>Bepul</b>: 100 Shijoat/kun\n\n"
    "💎 <b>Premium</b> — {premium_price}:\n"
    "• 1,000 Shijoat/kun\n"
    "• Barcha darslar ochiq\n\n"
    "♾️ <b>Cheksiz (deyarli)</b> — {unlimited_price}:\n"
    "• 9,999 Shijoat/kun (deyarli cheksiz)\n"
    "• Barcha imkoniyatlar\n\n"
    "🐪 Tuyavoy: Quyidan tanlang:"
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
PAYMENT_SENT = "Chekingiz adminga yuborildi! ✅\n\n🐪 Tuyavoy: Tez orada tasdiqlanadi. Biroz kuting! 🙏"

PAYMENT_APPROVED = (
    "🐪 Tuyavoy: Tabriklaymiz! 🎉\n\n"
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
    "🐪 Tuyavoy: Salom, {name}! 🎁\n\n"
    "Arab tili o'rganish loyihasiga xush kelibsiz — siz uchun <b>2 kunlik Premium sinov</b> "
    "bepul berildi!\n\n"
    "⚡ Bugun <b>1,000 Shijoat</b> bilan dars qiling!\n"
    "📅 Sinov muddati: bugun va ertaga\n\n"
    "Arab tilini o'rganishda muvaffaqiyatlar tilaymiz! 💪🌟"
)

SUBSCRIPTION_EXPIRED = (
    "🐪 Tuyavoy: Sizning <b>{tier_name}</b> obunangiz tugadi. ⏰\n\n"
    "Endi kuniga 100 Shijoat bilan davom etamiz.\n\n"
    "Streak va natijalaringizni saqlab, obunani yangilashingiz mumkin! 🔥"
)

SUBSCRIPTION_EXPIRES_SOON = (
    "🐪 Tuyavoy: Sizning <b>{tier_name}</b> obunangiz <b>{days}</b> kunda tugaydi! ⏰\n\n"
    "Obunani yangilab, o'rganishni uzluksiz davom ettiring qadrligim. 💪"
)

REMINDER_MESSAGES = [
    "🐪 Tuyavoy: Arab tili sizni kutyapti! Bugungi shijoat ballaringizdan foydalaning! 🔥",
    "🐪 Tuyavoy: Atigi 5 daqiqa — va bugungi darsni yakunlaysiz. Streakni yo'qotmang! ⏳📚",
    "🐪 Tuyavoy: Bilim — boylik. Bugungi darsni o'tkazib yubormang! 📖✨",
    "🐪 Tuyavoy: Bugun dars qildingizmi? Streakni davom ettiring! 🔥📖",
    "🐪 Tuyavoy: Bilim yo'lida har kun bir qadam! Bugungi darsni boshlang. 💪",
]

ROADMAP_HEADER = "🗺 <b>O'quv yo'lxaritasi</b>\n\n"
ROADMAP_LEVEL_DONE = "✅ <b>{n}-daraja</b> — {title}\n   {bar} {pct}% o'zlashtirilgan\n\n"
ROADMAP_LEVEL_CURRENT = "🎯 <b>{n}-daraja</b> — {title}  ← Joriy\n   {bar} {pct}%\n\n"
ROADMAP_LEVEL_NEXT = "🔓 <b>{n}-daraja</b> — {title}\n   Ochiq (hali boshlanmagan)\n\n"
ROADMAP_LEVEL_LOCKED = "🔒 <b>{n}-daraja</b> — {title}\n   {prev}-darajani yakunlang\n\n"
ROADMAP_TOPIC_ROW = "      {icon} Mavzu {n}: {name}  {bar} {pct}%  {marker}\n"
ROADMAP_TOPIC_LOCKED = "      🔒 Mavzu {n}: {name}  (oldingi mavzuni tugating)\n"

ACHIEVEMENT_EARNED = "🏆 <b>Yangi yutuq!</b>\n\n{name}\n<i>{desc}</i>"

# ── Referral messages ─────────────────────────────────────────────────────────

REFERRAL_INFO = (
    "🐪 Tuyavoy: Do'stingizni taklif qiling — ikkalangiz ham 500 Shijoat olasiz!\n\n"
    "🔗 Havola: {link}\n\n"
    "📋 Bir kunda necha do'st taklif qilsangiz ham bo'ladi!"
)

REFERRAL_RECEIVED = (
    "🐪 Tuyavoy: Tabriklaymiz! {referrer_name} sizni taklif qildi — "
    "ikkalangizga ham +500 Shijoat qo'shildi! 🎁"
)

REFERRAL_SUCCESS = (
    "🐪 Tuyavoy: Zo'r! {name} sizning taklif havolangiz orqali qo'shildi — "
    "sizga +500 Shijoat qo'shildi! 🎁"
)

# ── Daily goal messages ───────────────────────────────────────────────────────

DAILY_GOAL_PROGRESS = (
    "🐪 Tuyavoy: Bugun {done}/3 dars bajardingiz! {emoji}\n{msg}"
)

DAILY_GOAL_DONE = (
    "🐪 Tuyavoy: 🎉 Bugungi 3 ta dars maqsadini bajardingiz! Siz zo'rsiz! 💪\n"
    "Ertaga yana kutaman!"
)

# ── Achievement broadcast & congrats ─────────────────────────────────────────

ACHIEVEMENT_BROADCAST = (
    "🏆 <b>{name}</b> yangi yutuqqa erishdi!\n\n"
    "🌟 <b>{ach_name}</b>\n"
    "<i>{ach_desc}</i>\n\n"
    "🐪 Tuyavoy: Ilm yo'lida ildamlayotganlarga hurmatimiz baland! Uni tabriklang 👇"
)

CONGRAT_SENT = (
    "🐪 Tuyavoy: {sender_name} sizi <b>{ach_name}</b> yutug'ingiz bilan tabrikladilar! 🎊"
)

CONGRAT_TOAST = "🎊 Tabriklaringiz yetkazildi! Tuyavoy ham sizdan mamnun 🐪"

# ── Leaderboard messages ──────────────────────────────────────────────────────

LEADERBOARD_HEADER = "🏆 <b>{period} Reyting — Top 10</b> 💎\n\n"

DAILY_COMPARE = "🐪 Tuyavoy: {fact}"

TUYAVOY_FACTS = [
    "Arab tili dunyodagi eng qadimiy tillardan biri — 1500+ yillik tarix! Sen uni o'rganayapsan, bu zo'r!",
    "Arabcha o'ngdan chapga yoziladi — miyangiz endi ikki yo'nalishda ishlaydi!",
    "Arabchada 28 ta harf bor. Sen allaqachon bir nechtasini bilasan!",
    "Qur'on arabchada yozilgan — bu til 1.8 milliard insonning qalbida yashaydi.",
    "Arabcha so'zlar Inglizcha, O'zbekcha va ko'p tillarga kirgan: algebra, kimyo, qahva!",
    "Har kuni bir so'z o'rgansang — yilda 365 so'z! Sen esa bir darsda o'ndan ortiq o'rganasan!",
    "Tuyavoy cho'lda 7 kun suvsiz yashaydi — sen ham har kuni dars qilsang, maqsadga yetasan!",
    "Arab tilida 'ilm' so'zi 'bilim' degani — va bilim olish hech qachon to'xtamaydi!",
    "Streaking — dars ketma-ket davom ettirish — miyangizni kuchaytiradi! Davom et!",
    "Arabcha o'rganish boshqa tillarni ham osonlashtiradi — eron, turk, urdu...",
    "Har to'g'ri javob uchun miyangizda yangi ulanish hosil bo'ladi. Bugun nechta ulandingiz?",
    "Tuyavoy Sahara cho'lida 500 so'z yodlagan — sen ham uddalaysan!",
    "Arabcha musiqasi go'zal — 'marhaban' deb aytganingizda bir dunyo ochiladi!",
    "Dunyoda 400 milliondan ortiq odam arabcha gapiradi — siz ham ularning safiga qo'shilayapsiz!",
    "Har dars — bir qadam. Har so'z — bir g'isht. Bir kun qarasang — qal'a qurilgan bo'ladi! 🏰",
]

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
    "2+ kun streakda +10 Olmos bonus. "
    "Bir kun o'tkazib yuborsangiz — streak noldan boshlanadi.\n\n"

    "<b>💎 Olmos va unvonlar</b>\n"
    "Har to'g'ri javob +5 Olmos, dars yakunida +30 Olmos bonus. "
    "Olmos to'plash bilan unvon ko'tariladi "
    "(Yangi boshlovchi → Arab tili ustasi).\n\n"

    "<b>🏆 Yutuqlar</b>\n"
    "Birinchi dars, streak rekordlari, so'z milestones — "
    "har yutuqda maxsus nishon beriladi!\n\n"

    "<b>👥 Do'stlarni taklif qilish</b>\n"
    "Har taklif qilgan do'stingiz uchun ikkalangiz ham +500 Shijoat olasiz!"
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
    "💎 Olmos: {xp}\n"
    "🔥 Streak: {streak} kun\n"
    "⚡ Shijoat: {shijoat}\n"
    "🎫 Obuna: {tier}\n"
    "📅 Qo'shilgan: {join_date}\n"
    "🕐 Oxirgi faollik: {last_active}\n"
    "🚫 Bloklangan: {is_banned}"
)

BROADCAST_ASK = "Barcha foydalanuvchilarga yuboriladigan xabarni kiriting:"
BROADCAST_CONFIRM = "Xabar {count} ta foydalanuvchiga yuboriladi. Davom etasizmi?"
BROADCAST_DONE = "Xabar {sent}/{total} foydalanuvchiga yuborildi."
