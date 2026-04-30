"""
Vocabulary seed — pure Arabic language (Mabdaul Qiroat + Shifohiya).
No religious content.
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.database.base import engine, async_session_maker
from bot.database.models import Base, Vocabulary
from sqlalchemy import select

VOCABULARY = [
    # ══════════════════════════════════════════════════════════════
    # MODULE 1 — Alifbo (1-chi qism): ~42 ta so'z, 6 mavzu
    # Maqsad: foydalanuvchi 3-4 soat sarf qilsin
    # ══════════════════════════════════════════════════════════════

    # Mavzu 1: Harflar ا-خ (7 ta harf)
    {"level_id": 1, "topic_id": 1, "arabic_word": "ا", "uzbek_translation": "Alif harfi", "transliteration": "alif", "category": "harf"},
    {"level_id": 1, "topic_id": 1, "arabic_word": "ب", "uzbek_translation": "Ba harfi", "transliteration": "ba", "category": "harf"},
    {"level_id": 1, "topic_id": 1, "arabic_word": "ت", "uzbek_translation": "Ta harfi", "transliteration": "ta", "category": "harf"},
    {"level_id": 1, "topic_id": 1, "arabic_word": "ث", "uzbek_translation": "Sa harfi", "transliteration": "sa", "category": "harf"},
    {"level_id": 1, "topic_id": 1, "arabic_word": "ج", "uzbek_translation": "Jim harfi", "transliteration": "jim", "category": "harf"},
    {"level_id": 1, "topic_id": 1, "arabic_word": "ح", "uzbek_translation": "Ha harfi", "transliteration": "ha", "category": "harf"},
    {"level_id": 1, "topic_id": 1, "arabic_word": "خ", "uzbek_translation": "Xa harfi", "transliteration": "kha", "category": "harf"},

    # Mavzu 2: Birinchi so'zlar — eshik, taom, tabiat (7 ta)
    {"level_id": 1, "topic_id": 2, "arabic_word": "بَابٌ", "uzbek_translation": "🚪 Eshik", "transliteration": "baab", "category": "soz",
     "example_sentence_arabic": "هَذَا بَابٌ كَبِيرٌ", "example_sentence_uzbek": "Bu katta eshik"},
    {"level_id": 1, "topic_id": 2, "arabic_word": "تَمْرٌ", "uzbek_translation": "🌴 Xurmo", "transliteration": "tamr", "category": "soz"},
    {"level_id": 1, "topic_id": 2, "arabic_word": "جَبَلٌ", "uzbek_translation": "⛰️ Tog'", "transliteration": "jabal", "category": "soz"},
    {"level_id": 1, "topic_id": 2, "arabic_word": "حَجَرٌ", "uzbek_translation": "🪨 Tosh", "transliteration": "hajar", "category": "soz"},
    {"level_id": 1, "topic_id": 2, "arabic_word": "خُبْزٌ", "uzbek_translation": "🍞 Non", "transliteration": "khubz", "category": "soz"},
    {"level_id": 1, "topic_id": 2, "arabic_word": "أَبٌ", "uzbek_translation": "👨 Ota", "transliteration": "ab", "category": "soz",
     "example_sentence_arabic": "هَذَا أَبِي", "example_sentence_uzbek": "Bu mening otam"},
    {"level_id": 1, "topic_id": 2, "arabic_word": "أُمٌّ", "uzbek_translation": "👩 Ona", "transliteration": "umm", "category": "soz",
     "example_sentence_arabic": "هَذِهِ أُمِّي", "example_sentence_uzbek": "Bu mening onam"},

    # Mavzu 3: Jism a'zolari (7 ta)
    {"level_id": 1, "topic_id": 3, "arabic_word": "رَأْسٌ", "uzbek_translation": "🗣️ Bosh", "transliteration": "ra's", "category": "soz"},
    {"level_id": 1, "topic_id": 3, "arabic_word": "عَيْنٌ", "uzbek_translation": "👁️ Ko'z", "transliteration": "ayn", "category": "soz"},
    {"level_id": 1, "topic_id": 3, "arabic_word": "أَنْفٌ", "uzbek_translation": "👃 Burun", "transliteration": "anf", "category": "soz"},
    {"level_id": 1, "topic_id": 3, "arabic_word": "يَدٌ", "uzbek_translation": "✋ Qo'l", "transliteration": "yad", "category": "soz"},
    {"level_id": 1, "topic_id": 3, "arabic_word": "رِجْلٌ", "uzbek_translation": "🦵 Oyoq", "transliteration": "rijl", "category": "soz"},
    {"level_id": 1, "topic_id": 3, "arabic_word": "أُذُنٌ", "uzbek_translation": "👂 Quloq", "transliteration": "uzun", "category": "soz"},
    {"level_id": 1, "topic_id": 3, "arabic_word": "فَمٌ", "uzbek_translation": "👄 Og'iz", "transliteration": "fam", "category": "soz"},

    # Mavzu 4: Ranglar (7 ta)
    {"level_id": 1, "topic_id": 4, "arabic_word": "أَحْمَرُ", "uzbek_translation": "🔴 Qizil", "transliteration": "ahmar", "category": "soz"},
    {"level_id": 1, "topic_id": 4, "arabic_word": "أَزْرَقُ", "uzbek_translation": "🔵 Ko'k", "transliteration": "azraq", "category": "soz"},
    {"level_id": 1, "topic_id": 4, "arabic_word": "أَخْضَرُ", "uzbek_translation": "🟢 Yashil", "transliteration": "akhdar", "category": "soz"},
    {"level_id": 1, "topic_id": 4, "arabic_word": "أَصْفَرُ", "uzbek_translation": "🟡 Sariq", "transliteration": "asfar", "category": "soz"},
    {"level_id": 1, "topic_id": 4, "arabic_word": "أَبْيَضُ", "uzbek_translation": "⬜ Oq", "transliteration": "abyad", "category": "soz"},
    {"level_id": 1, "topic_id": 4, "arabic_word": "أَسْوَدُ", "uzbek_translation": "⬛ Qora", "transliteration": "aswad", "category": "soz"},
    {"level_id": 1, "topic_id": 4, "arabic_word": "بُرْتُقَالِيٌّ", "uzbek_translation": "🟠 To'q sariq", "transliteration": "burtuqaali", "category": "soz"},

    # Mavzu 5: Hayvonlar (7 ta)
    {"level_id": 1, "topic_id": 5, "arabic_word": "أَسَدٌ", "uzbek_translation": "🦁 Sher", "transliteration": "asad", "category": "soz"},
    {"level_id": 1, "topic_id": 5, "arabic_word": "فِيلٌ", "uzbek_translation": "🐘 Fil", "transliteration": "fiil", "category": "soz"},
    {"level_id": 1, "topic_id": 5, "arabic_word": "حِصَانٌ", "uzbek_translation": "🐴 Ot", "transliteration": "hisaan", "category": "soz"},
    {"level_id": 1, "topic_id": 5, "arabic_word": "بَقَرَةٌ", "uzbek_translation": "🐄 Sigir", "transliteration": "baqara", "category": "soz"},
    {"level_id": 1, "topic_id": 5, "arabic_word": "قِطٌّ", "uzbek_translation": "🐱 Mushuk", "transliteration": "qitt", "category": "soz"},
    {"level_id": 1, "topic_id": 5, "arabic_word": "كَلْبٌ", "uzbek_translation": "🐶 It", "transliteration": "kalb", "category": "soz"},
    {"level_id": 1, "topic_id": 5, "arabic_word": "عُصْفُورٌ", "uzbek_translation": "🐦 Chumchuq", "transliteration": "usfuur", "category": "soz"},

    # Mavzu 6: Raqamlar 1-7 (7 ta)
    {"level_id": 1, "topic_id": 6, "arabic_word": "وَاحِدٌ", "uzbek_translation": "1️⃣ Bir", "transliteration": "waahid", "category": "soz"},
    {"level_id": 1, "topic_id": 6, "arabic_word": "اثْنَانِ", "uzbek_translation": "2️⃣ Ikki", "transliteration": "ithnaan", "category": "soz"},
    {"level_id": 1, "topic_id": 6, "arabic_word": "ثَلَاثَةٌ", "uzbek_translation": "3️⃣ Uch", "transliteration": "thalaatha", "category": "soz"},
    {"level_id": 1, "topic_id": 6, "arabic_word": "أَرْبَعَةٌ", "uzbek_translation": "4️⃣ To'rt", "transliteration": "arba'a", "category": "soz"},
    {"level_id": 1, "topic_id": 6, "arabic_word": "خَمْسَةٌ", "uzbek_translation": "5️⃣ Besh", "transliteration": "khamsa", "category": "soz"},
    {"level_id": 1, "topic_id": 6, "arabic_word": "سِتَّةٌ", "uzbek_translation": "6️⃣ Olti", "transliteration": "sitta", "category": "soz"},
    {"level_id": 1, "topic_id": 6, "arabic_word": "سَبْعَةٌ", "uzbek_translation": "7️⃣ Yetti", "transliteration": "sab'a", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 2 — Alifbo (2-chi qism): ~42 ta so'z, 4 mavzu
    # ══════════════════════════════════════════════════════════════

    # Mavzu 1: Harflar د-ق (7 ta)
    {"level_id": 2, "topic_id": 1, "arabic_word": "د", "uzbek_translation": "Dal harfi", "transliteration": "dal", "category": "harf"},
    {"level_id": 2, "topic_id": 1, "arabic_word": "ذ", "uzbek_translation": "Zal harfi", "transliteration": "zal", "category": "harf"},
    {"level_id": 2, "topic_id": 1, "arabic_word": "ر", "uzbek_translation": "Ra harfi", "transliteration": "ra", "category": "harf"},
    {"level_id": 2, "topic_id": 1, "arabic_word": "ز", "uzbek_translation": "Zay harfi", "transliteration": "zay", "category": "harf"},
    {"level_id": 2, "topic_id": 1, "arabic_word": "س", "uzbek_translation": "Sin harfi", "transliteration": "sin", "category": "harf"},
    {"level_id": 2, "topic_id": 1, "arabic_word": "ش", "uzbek_translation": "Shin harfi", "transliteration": "shin", "category": "harf"},
    {"level_id": 2, "topic_id": 1, "arabic_word": "ص", "uzbek_translation": "Sod harfi", "transliteration": "sad", "category": "harf"},

    # Mavzu 2: Harflar ض-ق (7 ta)
    {"level_id": 2, "topic_id": 2, "arabic_word": "ض", "uzbek_translation": "Zod harfi", "transliteration": "dad", "category": "harf"},
    {"level_id": 2, "topic_id": 2, "arabic_word": "ط", "uzbek_translation": "To' harfi", "transliteration": "ta mufakhkhama", "category": "harf"},
    {"level_id": 2, "topic_id": 2, "arabic_word": "ظ", "uzbek_translation": "Zo' harfi", "transliteration": "za mufakhkhama", "category": "harf"},
    {"level_id": 2, "topic_id": 2, "arabic_word": "ع", "uzbek_translation": "Ayn harfi", "transliteration": "ayn", "category": "harf"},
    {"level_id": 2, "topic_id": 2, "arabic_word": "غ", "uzbek_translation": "G'ayn harfi", "transliteration": "ghain", "category": "harf"},
    {"level_id": 2, "topic_id": 2, "arabic_word": "ف", "uzbek_translation": "Fa harfi", "transliteration": "fa", "category": "harf"},
    {"level_id": 2, "topic_id": 2, "arabic_word": "ق", "uzbek_translation": "Qof harfi", "transliteration": "qaf", "category": "harf"},

    # Mavzu 3: Tabiat va kundalik (7 ta)
    {"level_id": 2, "topic_id": 3, "arabic_word": "دَارٌ", "uzbek_translation": "🏡 Katta uy", "transliteration": "daar", "category": "soz",
     "example_sentence_arabic": "هَذِهِ دَارٌ جَمِيلَةٌ", "example_sentence_uzbek": "Bu chiroyli katta uy"},
    {"level_id": 2, "topic_id": 3, "arabic_word": "زَهْرَةٌ", "uzbek_translation": "🌸 Gul", "transliteration": "zahra", "category": "soz"},
    {"level_id": 2, "topic_id": 3, "arabic_word": "سَمَكٌ", "uzbek_translation": "🐟 Baliq", "transliteration": "samak", "category": "soz"},
    {"level_id": 2, "topic_id": 3, "arabic_word": "شَجَرَةٌ", "uzbek_translation": "🌳 Daraxt", "transliteration": "shajara", "category": "soz"},
    {"level_id": 2, "topic_id": 3, "arabic_word": "طَيْرٌ", "uzbek_translation": "🐦 Qush", "transliteration": "tayr", "category": "soz"},
    {"level_id": 2, "topic_id": 3, "arabic_word": "قَمَرٌ", "uzbek_translation": "🌙 Oy (osmon)", "transliteration": "qamar", "category": "soz"},
    {"level_id": 2, "topic_id": 3, "arabic_word": "ضَوْءٌ", "uzbek_translation": "💡 Nur / Yorug'lik", "transliteration": "daw'", "category": "soz"},

    # Mavzu 4: Odamlar va narsalar (7 ta)
    {"level_id": 2, "topic_id": 4, "arabic_word": "رَجُلٌ", "uzbek_translation": "👨 Erkak", "transliteration": "rajul", "category": "soz"},
    {"level_id": 2, "topic_id": 4, "arabic_word": "صَدِيقٌ", "uzbek_translation": "🤝 Do'st", "transliteration": "sadiiq", "category": "soz",
     "example_sentence_arabic": "هُوَ صَدِيقِي", "example_sentence_uzbek": "U mening do'stim"},
    {"level_id": 2, "topic_id": 4, "arabic_word": "طِفْلٌ", "uzbek_translation": "👶 Bola", "transliteration": "tifl", "category": "soz"},
    {"level_id": 2, "topic_id": 4, "arabic_word": "ذَهَبٌ", "uzbek_translation": "✨ Oltin", "transliteration": "zahab", "category": "soz"},
    {"level_id": 2, "topic_id": 4, "arabic_word": "غَابَةٌ", "uzbek_translation": "🌲 O'rmon", "transliteration": "ghaaba", "category": "soz"},
    {"level_id": 2, "topic_id": 4, "arabic_word": "ظِلٌّ", "uzbek_translation": "🌑 Soya", "transliteration": "zill", "category": "soz"},
    {"level_id": 2, "topic_id": 4, "arabic_word": "صَخْرَةٌ", "uzbek_translation": "🪨 Qoya", "transliteration": "sakhrah", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 3 — Alifbo (3-chi qism) + Maktab + Uy + Tabiat: 5 mavzu
    # ══════════════════════════════════════════════════════════════

    # Mavzu 1: Harflar ك-ي va maxsus belgilar (7 ta)
    {"level_id": 3, "topic_id": 1, "arabic_word": "ك", "uzbek_translation": "Kof harfi", "transliteration": "kaf", "category": "harf"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "ل", "uzbek_translation": "Lom harfi", "transliteration": "lam", "category": "harf"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "م", "uzbek_translation": "Mim harfi", "transliteration": "mim", "category": "harf"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "ن", "uzbek_translation": "Nun harfi", "transliteration": "nun", "category": "harf"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "و", "uzbek_translation": "Vov harfi", "transliteration": "waw", "category": "harf"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "ه", "uzbek_translation": "Ha' harfi", "transliteration": "ha'", "category": "harf"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "ي", "uzbek_translation": "Ya harfi", "transliteration": "ya", "category": "harf"},

    # Mavzu 2: Maxsus harflar va hamzalar (7 ta)
    {"level_id": 3, "topic_id": 2, "arabic_word": "لا", "uzbek_translation": "Lom-Alif (maxsus shakl)", "transliteration": "lam-alif", "category": "harf"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "ء", "uzbek_translation": "Hamza harfi", "transliteration": "hamza", "category": "harf"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "آ", "uzbek_translation": "Alif Madd — uzun 'aa'", "transliteration": "alif madd", "category": "harf"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "أ", "uzbek_translation": "Hamza alif ustida", "transliteration": "hamzat al-qat'", "category": "harf"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "إ", "uzbek_translation": "Hamza alif ostida", "transliteration": "hamza kasriyya", "category": "harf"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "ؤ", "uzbek_translation": "Hamza vov ustida", "transliteration": "hamza 'ala waw", "category": "harf"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "ئ", "uzbek_translation": "Hamza ya ustida", "transliteration": "hamza 'ala ya", "category": "harf"},

    # Mavzu 3: Maktab so'zlari (7 ta)
    {"level_id": 3, "topic_id": 3, "arabic_word": "كِتَابٌ", "uzbek_translation": "📚 Kitob", "transliteration": "kitaab", "category": "soz",
     "example_sentence_arabic": "هَذَا كِتَابٌ جَدِيدٌ", "example_sentence_uzbek": "Bu yangi kitob"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "قَلَمٌ", "uzbek_translation": "✏️ Qalam", "transliteration": "qalam", "category": "soz",
     "example_sentence_arabic": "هَذَا قَلَمٌ أَحْمَرُ", "example_sentence_uzbek": "Bu qizil qalam"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "مَدْرَسَةٌ", "uzbek_translation": "🏫 Maktab", "transliteration": "madrasa", "category": "soz"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "مُعَلِّمٌ", "uzbek_translation": "👨‍🏫 O'qituvchi", "transliteration": "mu'allim", "category": "soz",
     "example_sentence_arabic": "الْمُعَلِّمُ فِي الْفَصْلِ", "example_sentence_uzbek": "O'qituvchi sinfda"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "طَالِبٌ", "uzbek_translation": "🎒 O'quvchi", "transliteration": "taalib", "category": "soz",
     "example_sentence_arabic": "هُوَ طَالِبٌ مُجْتَهِدٌ", "example_sentence_uzbek": "U tirishqoq o'quvchi"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "دَفْتَرٌ", "uzbek_translation": "📓 Daftar", "transliteration": "daftar", "category": "soz"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "سَبُّورَةٌ", "uzbek_translation": "🖊️ Doska", "transliteration": "sabboora", "category": "soz"},

    # Mavzu 4: Uy so'zlari (7 ta)
    {"level_id": 3, "topic_id": 4, "arabic_word": "بَيْتٌ", "uzbek_translation": "🏠 Uy", "transliteration": "bayt", "category": "soz",
     "example_sentence_arabic": "هَذَا بَيْتٌ كَبِيرٌ", "example_sentence_uzbek": "Bu katta uy"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "مَطْبَخٌ", "uzbek_translation": "🍳 Oshxona", "transliteration": "matbakh", "category": "soz"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "غُرْفَةٌ", "uzbek_translation": "🛏️ Xona", "transliteration": "ghurfa", "category": "soz"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "مِفْتَاحٌ", "uzbek_translation": "🔑 Kalit", "transliteration": "miftaah", "category": "soz"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "نَافِذَةٌ", "uzbek_translation": "🪟 Deraza", "transliteration": "naafiза", "category": "soz"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "كُرْسِيٌّ", "uzbek_translation": "🪑 Stul", "transliteration": "kursi", "category": "soz"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "مِصْبَاحٌ", "uzbek_translation": "💡 Chiroq", "transliteration": "misbaaH", "category": "soz"},

    # Mavzu 5: Tabiiyat va ob-havo (7 ta)
    {"level_id": 3, "topic_id": 5, "arabic_word": "بَحْرٌ", "uzbek_translation": "🌊 Dengiz", "transliteration": "bahr", "category": "soz"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "نَهْرٌ", "uzbek_translation": "🏞️ Daryo", "transliteration": "nahr", "category": "soz"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "مَطَرٌ", "uzbek_translation": "🌧️ Yomg'ir", "transliteration": "matar", "category": "soz"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "ثَلْجٌ", "uzbek_translation": "❄️ Qor", "transliteration": "thalj", "category": "soz"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "هَوَاءٌ", "uzbek_translation": "💨 Havo", "transliteration": "hawaa", "category": "soz"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "وَرْدَةٌ", "uzbek_translation": "🌹 Atirgul", "transliteration": "warda", "category": "soz"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "عُشْبٌ", "uzbek_translation": "🌿 O't / Maysazor", "transliteration": "ushb", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 4 — Harakatlar (unli belgilari): 1 mavzu
    # ══════════════════════════════════════════════════════════════
    {"level_id": 4, "topic_id": 1, "arabic_word": "بَ", "uzbek_translation": "Fatha — 'a' tovushi (ba)", "transliteration": "fatha, ba", "category": "harakat"},
    {"level_id": 4, "topic_id": 1, "arabic_word": "بِ", "uzbek_translation": "Kasra — 'i' tovushi (bi)", "transliteration": "kasra, bi", "category": "harakat"},
    {"level_id": 4, "topic_id": 1, "arabic_word": "بُ", "uzbek_translation": "Damma — 'u' tovushi (bu)", "transliteration": "damma, bu", "category": "harakat"},
    {"level_id": 4, "topic_id": 1, "arabic_word": "بْ", "uzbek_translation": "Sukun — unli yo'q (b)", "transliteration": "sukun, b", "category": "harakat"},
    {"level_id": 4, "topic_id": 1, "arabic_word": "بً", "uzbek_translation": "Tanvin fatha — 'an' (ban)", "transliteration": "tanwin fatha, ban", "category": "harakat"},
    {"level_id": 4, "topic_id": 1, "arabic_word": "بٍ", "uzbek_translation": "Tanvin kasra — 'in' (bin)", "transliteration": "tanwin kasra, bin", "category": "harakat"},
    {"level_id": 4, "topic_id": 1, "arabic_word": "بٌ", "uzbek_translation": "Tanvin damma — 'un' (bun)", "transliteration": "tanwin damma, bun", "category": "harakat"},
    {"level_id": 4, "topic_id": 1, "arabic_word": "بّ", "uzbek_translation": "Shadda — harf ikkilanadi (bb)", "transliteration": "shadda, bb", "category": "harakat"},
    {"level_id": 4, "topic_id": 1, "arabic_word": "بَا", "uzbek_translation": "Madd alif — uzun 'aa' (baa)", "transliteration": "madd alif, baa", "category": "harakat"},
    {"level_id": 4, "topic_id": 1, "arabic_word": "بِي", "uzbek_translation": "Madd ya — uzun 'ii' (bii)", "transliteration": "madd ya, bii", "category": "harakat"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 5 — Oddiy so'zlar (1): 1 mavzu
    # ══════════════════════════════════════════════════════════════
    {"level_id": 5, "topic_id": 1, "arabic_word": "شَجَرَةٌ", "uzbek_translation": "🌳 Daraxt", "transliteration": "shajara", "category": "soz"},
    {"level_id": 5, "topic_id": 1, "arabic_word": "سَمَاءٌ", "uzbek_translation": "🌤️ Osmon", "transliteration": "samaa", "category": "soz"},
    {"level_id": 5, "topic_id": 1, "arabic_word": "أَرْضٌ", "uzbek_translation": "🌍 Yer / Zamin", "transliteration": "ard", "category": "soz"},
    {"level_id": 5, "topic_id": 1, "arabic_word": "مَاءٌ", "uzbek_translation": "💧 Suv", "transliteration": "maa", "category": "soz"},
    {"level_id": 5, "topic_id": 1, "arabic_word": "نَارٌ", "uzbek_translation": "🔥 Olov", "transliteration": "naar", "category": "soz"},
    {"level_id": 5, "topic_id": 1, "arabic_word": "شَمْسٌ", "uzbek_translation": "☀️ Quyosh", "transliteration": "shams", "category": "soz"},
    {"level_id": 5, "topic_id": 1, "arabic_word": "رِيحٌ", "uzbek_translation": "🌬️ Shamol", "transliteration": "riih", "category": "soz"},
    {"level_id": 5, "topic_id": 1, "arabic_word": "لَيْلٌ", "uzbek_translation": "🌙 Kecha / Tun", "transliteration": "layl", "category": "soz"},
    {"level_id": 5, "topic_id": 1, "arabic_word": "نَهَارٌ", "uzbek_translation": "☀️ Kunduz", "transliteration": "nahaar", "category": "soz"},
    {"level_id": 5, "topic_id": 1, "arabic_word": "وَقْتٌ", "uzbek_translation": "⏰ Vaqt", "transliteration": "waqt", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 6 — Salomlashish + Oila: 1 mavzu
    # ══════════════════════════════════════════════════════════════
    {"level_id": 6, "topic_id": 1, "arabic_word": "مَرْحَبًا", "uzbek_translation": "👋 Salom", "transliteration": "marhaban", "category": "soz"},
    {"level_id": 6, "topic_id": 1, "arabic_word": "أَهْلًا", "uzbek_translation": "🤝 Ahlan", "transliteration": "ahlan", "category": "soz"},
    {"level_id": 6, "topic_id": 1, "arabic_word": "صَبَاحُ الْخَيْرِ", "uzbek_translation": "🌅 Xayrli tong", "transliteration": "sabaah al-khayr", "category": "soz"},
    {"level_id": 6, "topic_id": 1, "arabic_word": "مَسَاءُ الْخَيْرِ", "uzbek_translation": "🌆 Xayrli kech", "transliteration": "masaa al-khayr", "category": "soz"},
    {"level_id": 6, "topic_id": 1, "arabic_word": "شُكْرًا", "uzbek_translation": "🙏 Rahmat", "transliteration": "shukran", "category": "soz"},
    {"level_id": 6, "topic_id": 1, "arabic_word": "عَفْوًا", "uzbek_translation": "🫶 Iltimos / Marhamat", "transliteration": "afwan", "category": "soz"},
    {"level_id": 6, "topic_id": 1, "arabic_word": "مَعَ السَّلَامَةِ", "uzbek_translation": "👋 Xayr / Ko'rishguncha", "transliteration": "maa as-salaama", "category": "soz"},
    {"level_id": 6, "topic_id": 1, "arabic_word": "أُسْرَةٌ", "uzbek_translation": "👨‍👩‍👧 Oila", "transliteration": "usra", "category": "soz"},
    {"level_id": 6, "topic_id": 1, "arabic_word": "وَلَدٌ", "uzbek_translation": "👦 Bola (o'g'il)", "transliteration": "walad", "category": "soz"},
    {"level_id": 6, "topic_id": 1, "arabic_word": "بِنْتٌ", "uzbek_translation": "👧 Qiz", "transliteration": "bint", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 7 — Olmoshlar: 1 mavzu
    # ══════════════════════════════════════════════════════════════
    {"level_id": 7, "topic_id": 1, "arabic_word": "أَنَا", "uzbek_translation": "🙋 Men", "transliteration": "ana", "category": "zamir",
     "example_sentence_arabic": "أَنَا طَالِبٌ", "example_sentence_uzbek": "Men talabaman"},
    {"level_id": 7, "topic_id": 1, "arabic_word": "أَنْتَ", "uzbek_translation": "👉 Sen (erkak)", "transliteration": "anta", "category": "zamir",
     "example_sentence_arabic": "أَنْتَ طَالِبٌ", "example_sentence_uzbek": "Sen talabasan"},
    {"level_id": 7, "topic_id": 1, "arabic_word": "أَنْتِ", "uzbek_translation": "👉 Sen (ayol)", "transliteration": "anti", "category": "zamir"},
    {"level_id": 7, "topic_id": 1, "arabic_word": "هُوَ", "uzbek_translation": "👨 U (erkak)", "transliteration": "huwa", "category": "zamir"},
    {"level_id": 7, "topic_id": 1, "arabic_word": "هِيَ", "uzbek_translation": "👩 U (ayol)", "transliteration": "hiya", "category": "zamir"},
    {"level_id": 7, "topic_id": 1, "arabic_word": "نَحْنُ", "uzbek_translation": "👥 Biz", "transliteration": "nahnu", "category": "zamir"},
    {"level_id": 7, "topic_id": 1, "arabic_word": "هُمْ", "uzbek_translation": "👥 Ular", "transliteration": "hum", "category": "zamir"},
    {"level_id": 7, "topic_id": 1, "arabic_word": "هَذَا", "uzbek_translation": "👆 Bu (erkak)", "transliteration": "haaza", "category": "zamir",
     "example_sentence_arabic": "هَذَا كِتَابٌ", "example_sentence_uzbek": "Bu kitob"},
    {"level_id": 7, "topic_id": 1, "arabic_word": "هَذِهِ", "uzbek_translation": "👆 Bu (ayol)", "transliteration": "haazihi", "category": "zamir"},
    {"level_id": 7, "topic_id": 1, "arabic_word": "ذَلِكَ", "uzbek_translation": "👇 U / Ul (uzoq)", "transliteration": "zaalika", "category": "zamir"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 8 — Sifatlar: 1 mavzu
    # ══════════════════════════════════════════════════════════════
    {"level_id": 8, "topic_id": 1, "arabic_word": "كَبِيرٌ", "uzbek_translation": "🔵 Katta", "transliteration": "kabiir", "category": "sifat",
     "example_sentence_arabic": "هَذَا بَيْتٌ كَبِيرٌ", "example_sentence_uzbek": "Bu katta uy"},
    {"level_id": 8, "topic_id": 1, "arabic_word": "صَغِيرٌ", "uzbek_translation": "🔹 Kichik", "transliteration": "saghiir", "category": "sifat",
     "example_sentence_arabic": "هَذَا كِتَابٌ صَغِيرٌ", "example_sentence_uzbek": "Bu kichik kitob"},
    {"level_id": 8, "topic_id": 1, "arabic_word": "جَدِيدٌ", "uzbek_translation": "✨ Yangi", "transliteration": "jadiid", "category": "sifat"},
    {"level_id": 8, "topic_id": 1, "arabic_word": "قَدِيمٌ", "uzbek_translation": "🕰️ Eski", "transliteration": "qadiim", "category": "sifat"},
    {"level_id": 8, "topic_id": 1, "arabic_word": "جَمِيلٌ", "uzbek_translation": "😍 Chiroyli", "transliteration": "jamiil", "category": "sifat"},
    {"level_id": 8, "topic_id": 1, "arabic_word": "سَرِيعٌ", "uzbek_translation": "⚡ Tez", "transliteration": "sarii", "category": "sifat"},
    {"level_id": 8, "topic_id": 1, "arabic_word": "بَطِيءٌ", "uzbek_translation": "🐢 Sekin", "transliteration": "batii", "category": "sifat"},
    {"level_id": 8, "topic_id": 1, "arabic_word": "طَوِيلٌ", "uzbek_translation": "📏 Uzun / Baland", "transliteration": "tawiil", "category": "sifat"},
    {"level_id": 8, "topic_id": 1, "arabic_word": "قَصِيرٌ", "uzbek_translation": "📐 Qisqa / Past", "transliteration": "qasiir", "category": "sifat"},
    {"level_id": 8, "topic_id": 1, "arabic_word": "قَوِيٌّ", "uzbek_translation": "💪 Kuchli", "transliteration": "qawiyy", "category": "sifat"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 9 — Fe'llar (1): 1 mavzu
    # ══════════════════════════════════════════════════════════════
    {"level_id": 9, "topic_id": 1, "arabic_word": "ذَهَبَ", "uzbek_translation": "🚶 Ketdi", "transliteration": "zahaba", "category": "fel",
     "example_sentence_arabic": "ذَهَبَ الْوَلَدُ إِلَى الْبَيْتِ", "example_sentence_uzbek": "Bola uyga ketdi"},
    {"level_id": 9, "topic_id": 1, "arabic_word": "جَاءَ", "uzbek_translation": "🏃 Keldi", "transliteration": "jaa'a", "category": "fel",
     "example_sentence_arabic": "جَاءَ الطَّالِبُ إِلَى الْفَصْلِ", "example_sentence_uzbek": "Talaba sinfga keldi"},
    {"level_id": 9, "topic_id": 1, "arabic_word": "كَتَبَ", "uzbek_translation": "✍️ Yozdi", "transliteration": "kataba", "category": "fel",
     "example_sentence_arabic": "كَتَبَ الْوَلَدُ الدَّرْسَ", "example_sentence_uzbek": "Bola darsni yozdi"},
    {"level_id": 9, "topic_id": 1, "arabic_word": "قَرَأَ", "uzbek_translation": "📖 O'qidi", "transliteration": "qara'a", "category": "fel",
     "example_sentence_arabic": "قَرَأَ الطَّالِبُ الْكِتَابَ", "example_sentence_uzbek": "Talaba kitobni o'qidi"},
    {"level_id": 9, "topic_id": 1, "arabic_word": "أَكَلَ", "uzbek_translation": "🍽️ Yedi", "transliteration": "akala", "category": "fel"},
    {"level_id": 9, "topic_id": 1, "arabic_word": "شَرِبَ", "uzbek_translation": "🥤 Ichdi", "transliteration": "shariba", "category": "fel"},
    {"level_id": 9, "topic_id": 1, "arabic_word": "جَلَسَ", "uzbek_translation": "🪑 O'tirdi", "transliteration": "jalasa", "category": "fel"},
    {"level_id": 9, "topic_id": 1, "arabic_word": "نَامَ", "uzbek_translation": "😴 Uxladi", "transliteration": "naama", "category": "fel"},
    {"level_id": 9, "topic_id": 1, "arabic_word": "فَتَحَ", "uzbek_translation": "🚪 Ochdi", "transliteration": "fataha", "category": "fel"},
    {"level_id": 9, "topic_id": 1, "arabic_word": "دَخَلَ", "uzbek_translation": "🏠 Kirdi", "transliteration": "dakhala", "category": "fel",
     "example_sentence_arabic": "دَخَلَ الْوَلَدُ الْغُرْفَةَ", "example_sentence_uzbek": "Bola xonaga kirdi"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 10 — Fe'llar (2): 1 mavzu
    # ══════════════════════════════════════════════════════════════
    {"level_id": 10, "topic_id": 1, "arabic_word": "خَرَجَ", "uzbek_translation": "🚶 Chiqdi", "transliteration": "kharaja", "category": "fel",
     "example_sentence_arabic": "خَرَجَ الْوَلَدُ مِنَ الْبَيْتِ", "example_sentence_uzbek": "Bola uydan chiqdi"},
    {"level_id": 10, "topic_id": 1, "arabic_word": "رَجَعَ", "uzbek_translation": "🔄 Qaytdi", "transliteration": "raja'a", "category": "fel"},
    {"level_id": 10, "topic_id": 1, "arabic_word": "وَقَفَ", "uzbek_translation": "🛑 To'xtadi", "transliteration": "waqafa", "category": "fel"},
    {"level_id": 10, "topic_id": 1, "arabic_word": "رَكَضَ", "uzbek_translation": "🏃 Yugurdi", "transliteration": "rakada", "category": "fel"},
    {"level_id": 10, "topic_id": 1, "arabic_word": "نَظَرَ", "uzbek_translation": "👀 Qaradi", "transliteration": "nazara", "category": "fel"},
    {"level_id": 10, "topic_id": 1, "arabic_word": "سَمِعَ", "uzbek_translation": "👂 Eshitdi", "transliteration": "sami'a", "category": "fel"},
    {"level_id": 10, "topic_id": 1, "arabic_word": "تَكَلَّمَ", "uzbek_translation": "🗣️ Gapirdi", "transliteration": "takallama", "category": "fel",
     "example_sentence_arabic": "تَكَلَّمَ الرَّجُلُ بِالْعَرَبِيَّةِ", "example_sentence_uzbek": "Erkak arabcha gapirdi"},
    {"level_id": 10, "topic_id": 1, "arabic_word": "لَعِبَ", "uzbek_translation": "⚽ O'ynadi", "transliteration": "la'iba", "category": "fel"},
    {"level_id": 10, "topic_id": 1, "arabic_word": "عَمِلَ", "uzbek_translation": "💼 Ishladi", "transliteration": "'amila", "category": "fel"},
    {"level_id": 10, "topic_id": 1, "arabic_word": "ضَحِكَ", "uzbek_translation": "😄 Kuldi", "transliteration": "dahika", "category": "fel"},
]


RELIGIOUS_CATEGORIES = {"islom", "dua"}
RELIGIOUS_WORDS = {
    "بِسْمِ اللَّهِ", "الْحَمْدُ لِلَّهِ", "سُبْحَانَ اللَّهِ",
    "اللَّهُ أَكْبَرُ", "لَا إِلَهَ إِلَّا اللَّهُ",
    "الصَّلَاةُ", "الصِّيَامُ", "الزَّكَاةُ", "الْحَجُّ",
    "الْقُرْآنُ", "الْإِيمَانُ",
}


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from sqlalchemy import delete, func, text
    async with async_session_maker() as session:
        try:
            await session.execute(text(
                "ALTER TABLE vocabulary ADD COLUMN IF NOT EXISTS topic_id INTEGER NOT NULL DEFAULT 1"
            ))
            await session.commit()
        except Exception:
            pass

        count = (await session.execute(
            select(func.count(Vocabulary.word_id))
        )).scalar() or 0

        if count > 0:
            sample = (await session.execute(select(Vocabulary).limit(20))).scalars().all()
            has_religious = any(
                w.category in RELIGIOUS_CATEGORIES or w.arabic_word in RELIGIOUS_WORDS
                for w in sample
            )
            max_topic = (await session.execute(
                select(func.max(Vocabulary.topic_id))
            )).scalar() or 1

            if has_religious or max_topic <= 1 or count < len(VOCABULARY):
                await session.execute(delete(Vocabulary))
                await session.commit()
                print("Wiped old vocabulary — re-seeding with expanded topic content.")
            else:
                print(f"Vocabulary already populated ({count} words). Skipping.")
                return

        for item in VOCABULARY:
            session.add(Vocabulary(**item))
        await session.commit()
        print(f"Seeded {len(VOCABULARY)} vocabulary words across 10 levels.")


if __name__ == "__main__":
    asyncio.run(seed())
