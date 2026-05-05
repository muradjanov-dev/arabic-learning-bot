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
    # MODULE 2 — Mavzu 6: Harflar ك-ي (7 ta) [harflar faqat 1-2 modulda]
    # ══════════════════════════════════════════════════════════════
    {"level_id": 2, "topic_id": 6, "arabic_word": "ك", "uzbek_translation": "Kof harfi", "transliteration": "kaf", "category": "harf"},
    {"level_id": 2, "topic_id": 6, "arabic_word": "ل", "uzbek_translation": "Lom harfi", "transliteration": "lam", "category": "harf"},
    {"level_id": 2, "topic_id": 6, "arabic_word": "م", "uzbek_translation": "Mim harfi", "transliteration": "mim", "category": "harf"},
    {"level_id": 2, "topic_id": 6, "arabic_word": "ن", "uzbek_translation": "Nun harfi", "transliteration": "nun", "category": "harf"},
    {"level_id": 2, "topic_id": 6, "arabic_word": "و", "uzbek_translation": "Vov harfi", "transliteration": "waw", "category": "harf"},
    {"level_id": 2, "topic_id": 6, "arabic_word": "ه", "uzbek_translation": "Ha' harfi", "transliteration": "ha'", "category": "harf"},
    {"level_id": 2, "topic_id": 6, "arabic_word": "ي", "uzbek_translation": "Ya harfi", "transliteration": "ya", "category": "harf"},

    # MODULE 2 — Mavzu 7: Maxsus harflar va hamzalar (7 ta)
    {"level_id": 2, "topic_id": 7, "arabic_word": "لا", "uzbek_translation": "Lom-Alif (maxsus shakl)", "transliteration": "lam-alif", "category": "harf"},
    {"level_id": 2, "topic_id": 7, "arabic_word": "ء", "uzbek_translation": "Hamza harfi", "transliteration": "hamza", "category": "harf"},
    {"level_id": 2, "topic_id": 7, "arabic_word": "آ", "uzbek_translation": "Alif Madd — uzun 'aa'", "transliteration": "alif madd", "category": "harf"},
    {"level_id": 2, "topic_id": 7, "arabic_word": "أ", "uzbek_translation": "Hamza alif ustida", "transliteration": "hamzat al-qat'", "category": "harf"},
    {"level_id": 2, "topic_id": 7, "arabic_word": "إ", "uzbek_translation": "Hamza alif ostida", "transliteration": "hamza kasriyya", "category": "harf"},
    {"level_id": 2, "topic_id": 7, "arabic_word": "ؤ", "uzbek_translation": "Hamza vov ustida", "transliteration": "hamza 'ala waw", "category": "harf"},
    {"level_id": 2, "topic_id": 7, "arabic_word": "ئ", "uzbek_translation": "Hamza ya ustida", "transliteration": "hamza 'ala ya", "category": "harf"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 3 — Lug'at: Maktab + Uy + Tabiat + Meva + Narsalar: 5 mavzu
    # ══════════════════════════════════════════════════════════════

    # Mavzu 1: Maktab so'zlari (7 ta)
    {"level_id": 3, "topic_id": 1, "arabic_word": "كِتَابٌ", "uzbek_translation": "📚 Kitob", "transliteration": "kitaabun", "category": "soz",
     "example_sentence_arabic": "هَذَا كِتَابٌ جَدِيدٌ", "example_sentence_uzbek": "Bu yangi kitob"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "قَلَمٌ", "uzbek_translation": "✏️ Qalam", "transliteration": "qalamun", "category": "soz",
     "example_sentence_arabic": "هَذَا قَلَمٌ أَحْمَرُ", "example_sentence_uzbek": "Bu qizil qalam"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "مَدْرَسَةٌ", "uzbek_translation": "🏫 Maktab", "transliteration": "madrasatun", "category": "soz"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "مُعَلِّمٌ", "uzbek_translation": "👨‍🏫 O'qituvchi", "transliteration": "mu'allimun", "category": "soz",
     "example_sentence_arabic": "الْمُعَلِّمُ فِي الْفَصْلِ", "example_sentence_uzbek": "O'qituvchi sinfda"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "طَالِبٌ", "uzbek_translation": "🎒 O'quvchi", "transliteration": "taalibun", "category": "soz",
     "example_sentence_arabic": "هُوَ طَالِبٌ مُجْتَهِدٌ", "example_sentence_uzbek": "U tirishqoq o'quvchi"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "دَفْتَرٌ", "uzbek_translation": "📓 Daftar", "transliteration": "daftarun", "category": "soz"},
    {"level_id": 3, "topic_id": 1, "arabic_word": "سَبُّورَةٌ", "uzbek_translation": "🖊️ Doska", "transliteration": "sabbooratun", "category": "soz"},

    # Mavzu 2: Uy so'zlari (7 ta)
    {"level_id": 3, "topic_id": 2, "arabic_word": "بَيْتٌ", "uzbek_translation": "🏠 Uy", "transliteration": "baytun", "category": "soz",
     "example_sentence_arabic": "هَذَا بَيْتٌ كَبِيرٌ", "example_sentence_uzbek": "Bu katta uy"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "مَطْبَخٌ", "uzbek_translation": "🍳 Oshxona", "transliteration": "matbakhun", "category": "soz"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "غُرْفَةٌ", "uzbek_translation": "🛏️ Xona", "transliteration": "ghurfatun", "category": "soz"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "مِفْتَاحٌ", "uzbek_translation": "🔑 Kalit", "transliteration": "miftaahun", "category": "soz"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "نَافِذَةٌ", "uzbek_translation": "🪟 Deraza", "transliteration": "naafiзatun", "category": "soz"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "كُرْسِيٌّ", "uzbek_translation": "🪑 Stul", "transliteration": "kursiyyun", "category": "soz"},
    {"level_id": 3, "topic_id": 2, "arabic_word": "مِصْبَاحٌ", "uzbek_translation": "💡 Chiroq", "transliteration": "misbaahun", "category": "soz"},

    # Mavzu 3: Tabiat va ob-havo (7 ta)
    {"level_id": 3, "topic_id": 3, "arabic_word": "بَحْرٌ", "uzbek_translation": "🌊 Dengiz", "transliteration": "bahrun", "category": "soz"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "نَهْرٌ", "uzbek_translation": "🏞️ Daryo", "transliteration": "nahrun", "category": "soz"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "مَطَرٌ", "uzbek_translation": "🌧️ Yomg'ir", "transliteration": "matarun", "category": "soz"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "ثَلْجٌ", "uzbek_translation": "❄️ Qor", "transliteration": "thaljun", "category": "soz"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "هَوَاءٌ", "uzbek_translation": "💨 Havo", "transliteration": "hawaa'un", "category": "soz"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "وَرْدَةٌ", "uzbek_translation": "🌹 Atirgul", "transliteration": "wardatun", "category": "soz"},
    {"level_id": 3, "topic_id": 3, "arabic_word": "عُشْبٌ", "uzbek_translation": "🌿 O't / Maysazor", "transliteration": "ushbun", "category": "soz"},

    # Mavzu 4: Mevalar va sabzavotlar (7 ta)
    {"level_id": 3, "topic_id": 4, "arabic_word": "تُفَّاحَةٌ", "uzbek_translation": "🍎 Olma", "transliteration": "tuffaahatun", "category": "soz"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "مَوْزٌ", "uzbek_translation": "🍌 Banan", "transliteration": "mawzun", "category": "soz"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "عِنَبٌ", "uzbek_translation": "🍇 Uzum", "transliteration": "'inabun", "category": "soz"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "بُرْتُقَالٌ", "uzbek_translation": "🍊 Apelsin", "transliteration": "burtuqaalun", "category": "soz",
     "example_sentence_arabic": "الْبُرْتُقَالُ حُلْوٌ", "example_sentence_uzbek": "Apelsin shirin"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "طَمَاطِمُ", "uzbek_translation": "🍅 Pomidor", "transliteration": "tamaatimu", "category": "soz"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "خِيَارٌ", "uzbek_translation": "🥒 Bodring", "transliteration": "khiyaarun", "category": "soz"},
    {"level_id": 3, "topic_id": 4, "arabic_word": "بَطَاطَا", "uzbek_translation": "🥔 Kartoshka", "transliteration": "bataaтaa", "category": "soz"},

    # Mavzu 5: Kundalik narsalar (7 ta)
    {"level_id": 3, "topic_id": 5, "arabic_word": "حَقِيبَةٌ", "uzbek_translation": "🎒 Sumka", "transliteration": "haqeebatun", "category": "soz",
     "example_sentence_arabic": "الْحَقِيبَةُ ثَقِيلَةٌ", "example_sentence_uzbek": "Sumka og'ir"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "سَاعَةٌ", "uzbek_translation": "⏰ Soat", "transliteration": "saa'atun", "category": "soz"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "هَاتِفٌ", "uzbek_translation": "📱 Telefon", "transliteration": "haatifun", "category": "soz"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "تِلْفَازٌ", "uzbek_translation": "📺 Televizor", "transliteration": "tilfaazun", "category": "soz"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "سَرِيرٌ", "uzbek_translation": "🛏️ Karavot", "transliteration": "sariirun", "category": "soz"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "طَاوِلَةٌ", "uzbek_translation": "🪑 Stol", "transliteration": "taаwilatun", "category": "soz",
     "example_sentence_arabic": "الْكِتَابُ عَلَى الطَّاوِلَةِ", "example_sentence_uzbek": "Kitob stolda"},
    {"level_id": 3, "topic_id": 5, "arabic_word": "مِرْآةٌ", "uzbek_translation": "🪞 Ko'zgu", "transliteration": "mir'aatun", "category": "soz"},

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
    # MODULE 5 — Oddiy so'zlar + Tabiat: 2 mavzu
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

    # Mavzu 2: Tabiat extended (8 ta)
    {"level_id": 5, "topic_id": 2, "arabic_word": "رِيَاضَةٌ", "uzbek_translation": "⚽ Sport", "transliteration": "riyaada", "category": "soz"},
    {"level_id": 5, "topic_id": 2, "arabic_word": "صِحَّةٌ", "uzbek_translation": "💪 Sog'liq", "transliteration": "sihha", "category": "soz"},
    {"level_id": 5, "topic_id": 2, "arabic_word": "لَوْنٌ", "uzbek_translation": "🎨 Rang", "transliteration": "lawn", "category": "soz"},
    {"level_id": 5, "topic_id": 2, "arabic_word": "صَوْتٌ", "uzbek_translation": "🔊 Ovoz", "transliteration": "sawt", "category": "soz"},
    {"level_id": 5, "topic_id": 2, "arabic_word": "حَرَارَةٌ", "uzbek_translation": "🌡️ Issiqlik", "transliteration": "haraara", "category": "soz"},
    {"level_id": 5, "topic_id": 2, "arabic_word": "بُرُودَةٌ", "uzbek_translation": "❄️ Sovuq", "transliteration": "buruuda", "category": "soz"},
    {"level_id": 5, "topic_id": 2, "arabic_word": "مَسَافَةٌ", "uzbek_translation": "📏 Masofa", "transliteration": "masaafa", "category": "soz"},
    {"level_id": 5, "topic_id": 2, "arabic_word": "سُرْعَةٌ", "uzbek_translation": "⚡ Tezlik", "transliteration": "sur'a", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 6 — Salomlashish + Oila: 2 mavzu
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

    # Mavzu 2: Oila extended (8 ta)
    {"level_id": 6, "topic_id": 2, "arabic_word": "أَخٌ", "uzbek_translation": "👦 Aka/Uka", "transliteration": "akh", "category": "soz",
     "example_sentence_arabic": "هَذَا أَخِي", "example_sentence_uzbek": "Bu mening akam"},
    {"level_id": 6, "topic_id": 2, "arabic_word": "أُخْتٌ", "uzbek_translation": "👧 Opa/Singil", "transliteration": "ukht", "category": "soz"},
    {"level_id": 6, "topic_id": 2, "arabic_word": "جَدٌّ", "uzbek_translation": "👴 Bobo", "transliteration": "jadd", "category": "soz"},
    {"level_id": 6, "topic_id": 2, "arabic_word": "جَدَّةٌ", "uzbek_translation": "👵 Buvi", "transliteration": "jadda", "category": "soz"},
    {"level_id": 6, "topic_id": 2, "arabic_word": "زَوْجٌ", "uzbek_translation": "👨 Er", "transliteration": "zawj", "category": "soz"},
    {"level_id": 6, "topic_id": 2, "arabic_word": "زَوْجَةٌ", "uzbek_translation": "👩 Xotin", "transliteration": "zawja", "category": "soz"},
    {"level_id": 6, "topic_id": 2, "arabic_word": "عَمٌّ", "uzbek_translation": "👨 Amaki", "transliteration": "amm", "category": "soz"},
    {"level_id": 6, "topic_id": 2, "arabic_word": "خَالٌ", "uzbek_translation": "👨 Tog'a", "transliteration": "khaal", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 7 — Olmoshlar: 2 mavzu
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

    # Mavzu 2: Savol so'zlari — Ko'rsatish olmoshlari (8 ta)
    {"level_id": 7, "topic_id": 2, "arabic_word": "مَنْ", "uzbek_translation": "❓ Kim?", "transliteration": "man", "category": "zamir",
     "example_sentence_arabic": "مَنْ هَذَا؟", "example_sentence_uzbek": "Bu kim?"},
    {"level_id": 7, "topic_id": 2, "arabic_word": "مَا", "uzbek_translation": "❓ Nima?", "transliteration": "maa", "category": "zamir",
     "example_sentence_arabic": "مَا هَذَا؟", "example_sentence_uzbek": "Bu nima?"},
    {"level_id": 7, "topic_id": 2, "arabic_word": "أَيْنَ", "uzbek_translation": "📍 Qayerda?", "transliteration": "ayna", "category": "zamir"},
    {"level_id": 7, "topic_id": 2, "arabic_word": "مَتَى", "uzbek_translation": "🕐 Qachon?", "transliteration": "mataa", "category": "zamir"},
    {"level_id": 7, "topic_id": 2, "arabic_word": "لِمَاذَا", "uzbek_translation": "🤔 Nima uchun?", "transliteration": "limaaza", "category": "zamir"},
    {"level_id": 7, "topic_id": 2, "arabic_word": "كَيْفَ", "uzbek_translation": "💭 Qanday?", "transliteration": "kayfa", "category": "zamir"},
    {"level_id": 7, "topic_id": 2, "arabic_word": "كَمْ", "uzbek_translation": "🔢 Qancha?", "transliteration": "kam", "category": "zamir"},
    {"level_id": 7, "topic_id": 2, "arabic_word": "هَلْ", "uzbek_translation": "❓ ...mi? (sual yuklamasi)", "transliteration": "hal", "category": "zamir",
     "example_sentence_arabic": "هَلْ أَنْتَ طَالِبٌ؟", "example_sentence_uzbek": "Sen talabamisan?"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 8 — Sifatlar: 2 mavzu
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

    # Mavzu 2: Zid sifatlar (8 ta)
    {"level_id": 8, "topic_id": 2, "arabic_word": "حَارٌّ", "uzbek_translation": "🔥 Issiq", "transliteration": "haar", "category": "sifat",
     "example_sentence_arabic": "الشَّايُ حَارٌّ", "example_sentence_uzbek": "Choy issiq"},
    {"level_id": 8, "topic_id": 2, "arabic_word": "بَارِدٌ", "uzbek_translation": "❄️ Sovuq", "transliteration": "baarid", "category": "sifat",
     "example_sentence_arabic": "الْمَاءُ بَارِدٌ", "example_sentence_uzbek": "Suv sovuq"},
    {"level_id": 8, "topic_id": 2, "arabic_word": "نَظِيفٌ", "uzbek_translation": "✨ Toza", "transliteration": "naziif", "category": "sifat"},
    {"level_id": 8, "topic_id": 2, "arabic_word": "وَسِخٌ", "uzbek_translation": "🪣 Iflos", "transliteration": "wasikh", "category": "sifat"},
    {"level_id": 8, "topic_id": 2, "arabic_word": "مُمْتَازٌ", "uzbek_translation": "🏆 A'lo", "transliteration": "mumtaaz", "category": "sifat",
     "example_sentence_arabic": "هَذَا طَالِبٌ مُمْتَازٌ", "example_sentence_uzbek": "Bu a'lo o'quvchi"},
    {"level_id": 8, "topic_id": 2, "arabic_word": "رَخِيصٌ", "uzbek_translation": "💰 Arzon", "transliteration": "rakhiis", "category": "sifat"},
    {"level_id": 8, "topic_id": 2, "arabic_word": "غَالٍ", "uzbek_translation": "💎 Qimmat", "transliteration": "ghaali", "category": "sifat"},
    {"level_id": 8, "topic_id": 2, "arabic_word": "مَرِيضٌ", "uzbek_translation": "🤒 Kasal", "transliteration": "mariid", "category": "sifat",
     "example_sentence_arabic": "هُوَ مَرِيضٌ الْيَوْمَ", "example_sentence_uzbek": "U bugun kasal"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 9 — Fe'llar (1): 2 mavzu
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

    # Mavzu 2: Fe'llar (holat) (8 ta)
    {"level_id": 9, "topic_id": 2, "arabic_word": "عَرَفَ", "uzbek_translation": "💡 Bildi", "transliteration": "arafa", "category": "fel",
     "example_sentence_arabic": "عَرَفَ الطَّالِبُ الْجَوَابَ", "example_sentence_uzbek": "Talaba javobni bildi"},
    {"level_id": 9, "topic_id": 2, "arabic_word": "فَكَّرَ", "uzbek_translation": "🤔 O'yladi", "transliteration": "fakkara", "category": "fel"},
    {"level_id": 9, "topic_id": 2, "arabic_word": "فَهِمَ", "uzbek_translation": "💭 Tushundi", "transliteration": "fahima", "category": "fel",
     "example_sentence_arabic": "فَهِمَ الدَّرْسَ", "example_sentence_uzbek": "Darsni tushundi"},
    {"level_id": 9, "topic_id": 2, "arabic_word": "أَحَبَّ", "uzbek_translation": "❤️ Sevdi", "transliteration": "ahabba", "category": "fel"},
    {"level_id": 9, "topic_id": 2, "arabic_word": "كَرِهَ", "uzbek_translation": "😠 Yomon ko'rdi", "transliteration": "kariha", "category": "fel"},
    {"level_id": 9, "topic_id": 2, "arabic_word": "خَافَ", "uzbek_translation": "😨 Qo'rqdi", "transliteration": "khaafa", "category": "fel"},
    {"level_id": 9, "topic_id": 2, "arabic_word": "فَرِحَ", "uzbek_translation": "😊 Xursand bo'ldi", "transliteration": "fariha", "category": "fel",
     "example_sentence_arabic": "فَرِحَ الْوَلَدُ بِالْهَدِيَّةِ", "example_sentence_uzbek": "Bola sovg'adan xursand bo'ldi"},
    {"level_id": 9, "topic_id": 2, "arabic_word": "حَزِنَ", "uzbek_translation": "😢 Qayg'urdi", "transliteration": "hazina", "category": "fel"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 10 — Fe'llar (2): 2 mavzu
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

    # Mavzu 2: Fe'llar (muloqot) (8 ta)
    {"level_id": 10, "topic_id": 2, "arabic_word": "سَأَلَ", "uzbek_translation": "❓ So'radi", "transliteration": "sa'ala", "category": "fel",
     "example_sentence_arabic": "سَأَلَ الطَّالِبُ الْمُعَلِّمَ", "example_sentence_uzbek": "Talaba o'qituvchidan so'radi"},
    {"level_id": 10, "topic_id": 2, "arabic_word": "أَجَابَ", "uzbek_translation": "✅ Javob berdi", "transliteration": "ajaaba", "category": "fel",
     "example_sentence_arabic": "أَجَابَ الْمُعَلِّمُ بِوُضُوحٍ", "example_sentence_uzbek": "O'qituvchi aniq javob berdi"},
    {"level_id": 10, "topic_id": 2, "arabic_word": "أَخْبَرَ", "uzbek_translation": "📢 Xabar berdi", "transliteration": "akhbara", "category": "fel"},
    {"level_id": 10, "topic_id": 2, "arabic_word": "نَادَى", "uzbek_translation": "📣 Chaqirdi", "transliteration": "naadaa", "category": "fel"},
    {"level_id": 10, "topic_id": 2, "arabic_word": "رَدَّ", "uzbek_translation": "↩️ Javob qaytardi", "transliteration": "radda", "category": "fel"},
    {"level_id": 10, "topic_id": 2, "arabic_word": "وَعَدَ", "uzbek_translation": "🤝 Va'da berdi", "transliteration": "wa'ada", "category": "fel",
     "example_sentence_arabic": "وَعَدَ بِالْمُسَاعَدَةِ", "example_sentence_uzbek": "Yordam berishga va'da berdi"},
    {"level_id": 10, "topic_id": 2, "arabic_word": "شَكَرَ", "uzbek_translation": "🙏 Minnatdorlik bildirdi", "transliteration": "shakara", "category": "fel"},
    {"level_id": 10, "topic_id": 2, "arabic_word": "اعْتَذَرَ", "uzbek_translation": "😔 Uzr so'radi", "transliteration": "i'tazara", "category": "fel",
     "example_sentence_arabic": "اعْتَذَرَ عَنِ التَّأَخُّرِ", "example_sentence_uzbek": "Kechikgani uchun uzr so'radi"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 2 — Mavzu 5: Raqamlar 8-100 (7 ta)
    # ══════════════════════════════════════════════════════════════
    {"level_id": 2, "topic_id": 5, "arabic_word": "ثَمَانِيَةٌ", "uzbek_translation": "8️⃣ Sakkiz", "transliteration": "thamaaniyatun", "category": "soz"},
    {"level_id": 2, "topic_id": 5, "arabic_word": "تِسْعَةٌ", "uzbek_translation": "9️⃣ To'qqiz", "transliteration": "tis'atun", "category": "soz"},
    {"level_id": 2, "topic_id": 5, "arabic_word": "عَشَرَةٌ", "uzbek_translation": "🔟 O'n", "transliteration": "asharatun", "category": "soz"},
    {"level_id": 2, "topic_id": 5, "arabic_word": "أَحَدَ عَشَرَ", "uzbek_translation": "1️⃣1️⃣ O'n bir", "transliteration": "ahada ashar", "category": "soz"},
    {"level_id": 2, "topic_id": 5, "arabic_word": "اثْنَا عَشَرَ", "uzbek_translation": "1️⃣2️⃣ O'n ikki", "transliteration": "ithnaa ashar", "category": "soz"},
    {"level_id": 2, "topic_id": 5, "arabic_word": "عِشْرُونَ", "uzbek_translation": "2️⃣0️⃣ Yigirma", "transliteration": "ishruuna", "category": "soz"},
    {"level_id": 2, "topic_id": 5, "arabic_word": "مِئَةٌ", "uzbek_translation": "💯 Yuz", "transliteration": "mi'atun", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 4 — Mavzu 2: ال ta'rif bilan so'zlar (7 ta)
    # ══════════════════════════════════════════════════════════════
    {"level_id": 4, "topic_id": 2, "arabic_word": "الْبَيْتُ", "uzbek_translation": "🏠 Uy (aniq)", "transliteration": "al-baytu", "category": "soz",
     "example_sentence_arabic": "الْبَيْتُ كَبِيرٌ", "example_sentence_uzbek": "Uy katta"},
    {"level_id": 4, "topic_id": 2, "arabic_word": "الْكِتَابُ", "uzbek_translation": "📚 Kitob (aniq)", "transliteration": "al-kitaabu", "category": "soz",
     "example_sentence_arabic": "الْكِتَابُ جَدِيدٌ", "example_sentence_uzbek": "Kitob yangi"},
    {"level_id": 4, "topic_id": 2, "arabic_word": "الْوَلَدُ", "uzbek_translation": "👦 Bola (aniq)", "transliteration": "al-waladu", "category": "soz",
     "example_sentence_arabic": "الْوَلَدُ صَغِيرٌ", "example_sentence_uzbek": "Bola kichik"},
    {"level_id": 4, "topic_id": 2, "arabic_word": "الشَّمْسُ", "uzbek_translation": "☀️ Quyosh (aniq)", "transliteration": "ash-shamsu", "category": "soz",
     "example_sentence_arabic": "الشَّمْسُ سَاطِعَةٌ", "example_sentence_uzbek": "Quyosh porlab turibdi"},
    {"level_id": 4, "topic_id": 2, "arabic_word": "الْقَمَرُ", "uzbek_translation": "🌙 Oy (aniq)", "transliteration": "al-qamaru", "category": "soz",
     "example_sentence_arabic": "الْقَمَرُ جَمِيلٌ", "example_sentence_uzbek": "Oy chiroyli"},
    {"level_id": 4, "topic_id": 2, "arabic_word": "الْمَاءُ", "uzbek_translation": "💧 Suv (aniq)", "transliteration": "al-maa'u", "category": "soz",
     "example_sentence_arabic": "الْمَاءُ بَارِدٌ", "example_sentence_uzbek": "Suv sovuq"},
    {"level_id": 4, "topic_id": 2, "arabic_word": "الرَّجُلُ", "uzbek_translation": "👨 Erkak (aniq)", "transliteration": "ar-rajulu", "category": "soz",
     "example_sentence_arabic": "الرَّجُلُ طَوِيلٌ", "example_sentence_uzbek": "Erkak baland bo'yli"},

    # MODULE 4 — Mavzu 3: Muzakkar va Muannath (7 ta)
    {"level_id": 4, "topic_id": 3, "arabic_word": "مُعَلِّمٌ", "uzbek_translation": "👨‍🏫 O'qituvchi (erkak)", "transliteration": "mu'allimun", "category": "soz",
     "example_sentence_arabic": "هُوَ مُعَلِّمٌ", "example_sentence_uzbek": "U o'qituvchi erkak"},
    {"level_id": 4, "topic_id": 3, "arabic_word": "مُعَلِّمَةٌ", "uzbek_translation": "👩‍🏫 O'qituvchi (ayol)", "transliteration": "mu'allimatun", "category": "soz",
     "example_sentence_arabic": "هِيَ مُعَلِّمَةٌ", "example_sentence_uzbek": "U o'qituvchi ayol"},
    {"level_id": 4, "topic_id": 3, "arabic_word": "طَالِبٌ", "uzbek_translation": "🎒 O'quvchi (erkak)", "transliteration": "taalibun", "category": "soz"},
    {"level_id": 4, "topic_id": 3, "arabic_word": "طَالِبَةٌ", "uzbek_translation": "🎒 O'quvchi (ayol)", "transliteration": "taalihatun", "category": "soz"},
    {"level_id": 4, "topic_id": 3, "arabic_word": "مُدِيرٌ", "uzbek_translation": "👔 Direktor (erkak)", "transliteration": "mudeerun", "category": "soz"},
    {"level_id": 4, "topic_id": 3, "arabic_word": "مُدِيرَةٌ", "uzbek_translation": "👔 Direktor (ayol)", "transliteration": "mudeeratun", "category": "soz"},
    {"level_id": 4, "topic_id": 3, "arabic_word": "طَبِيبٌ", "uzbek_translation": "👨‍⚕️ Shifokor", "transliteration": "tabeebun", "category": "soz",
     "example_sentence_arabic": "هُوَ طَبِيبٌ مَاهِرٌ", "example_sentence_uzbek": "U mohir shifokor"},

    # MODULE 4 — Mavzu 4: Taqniya / Ikkilik shakli (7 ta)
    {"level_id": 4, "topic_id": 4, "arabic_word": "كِتَابَانِ", "uzbek_translation": "📚📚 Ikki kitob", "transliteration": "kitaabaani", "category": "soz",
     "example_sentence_arabic": "عِنْدِي كِتَابَانِ", "example_sentence_uzbek": "Menda ikki kitob bor"},
    {"level_id": 4, "topic_id": 4, "arabic_word": "قَلَمَانِ", "uzbek_translation": "✏️✏️ Ikki qalam", "transliteration": "qalamaani", "category": "soz"},
    {"level_id": 4, "topic_id": 4, "arabic_word": "وَلَدَانِ", "uzbek_translation": "👦👦 Ikki bola", "transliteration": "waladaani", "category": "soz",
     "example_sentence_arabic": "هَذَانِ وَلَدَانِ", "example_sentence_uzbek": "Bu ikki bola"},
    {"level_id": 4, "topic_id": 4, "arabic_word": "يَدَانِ", "uzbek_translation": "✋✋ Ikki qo'l", "transliteration": "yadaani", "category": "soz"},
    {"level_id": 4, "topic_id": 4, "arabic_word": "عَيْنَانِ", "uzbek_translation": "👁️👁️ Ikki ko'z", "transliteration": "aynaani", "category": "soz"},
    {"level_id": 4, "topic_id": 4, "arabic_word": "يَوْمَانِ", "uzbek_translation": "📅📅 Ikki kun", "transliteration": "yawmaani", "category": "soz"},
    {"level_id": 4, "topic_id": 4, "arabic_word": "بَيْتَانِ", "uzbek_translation": "🏠🏠 Ikki uy", "transliteration": "baytaani", "category": "soz",
     "example_sentence_arabic": "هُنَاكَ بَيْتَانِ كَبِيرَانِ", "example_sentence_uzbek": "U yerda ikki katta uy bor"},

    # MODULE 4 — Mavzu 5: Ko'plik shakllari (7 ta)
    {"level_id": 4, "topic_id": 5, "arabic_word": "كُتُبٌ", "uzbek_translation": "📚 Kitoblar", "transliteration": "kutubun", "category": "soz",
     "example_sentence_arabic": "هَذِهِ كُتُبٌ كَثِيرَةٌ", "example_sentence_uzbek": "Bu ko'p kitoblar"},
    {"level_id": 4, "topic_id": 5, "arabic_word": "أَقْلَامٌ", "uzbek_translation": "✏️ Qalamlar", "transliteration": "aqlaamun", "category": "soz"},
    {"level_id": 4, "topic_id": 5, "arabic_word": "أَوْلَادٌ", "uzbek_translation": "👦 Bolalar", "transliteration": "awlaadun", "category": "soz",
     "example_sentence_arabic": "الْأَوْلَادُ فِي الْمَدْرَسَةِ", "example_sentence_uzbek": "Bolalar maktabda"},
    {"level_id": 4, "topic_id": 5, "arabic_word": "بَنَاتٌ", "uzbek_translation": "👧 Qizlar", "transliteration": "banaatun", "category": "soz"},
    {"level_id": 4, "topic_id": 5, "arabic_word": "رِجَالٌ", "uzbek_translation": "👨 Erkaklar", "transliteration": "rijaalun", "category": "soz"},
    {"level_id": 4, "topic_id": 5, "arabic_word": "بُيُوتٌ", "uzbek_translation": "🏠 Uylar", "transliteration": "buyootun", "category": "soz",
     "example_sentence_arabic": "الْبُيُوتُ كَبِيرَةٌ", "example_sentence_uzbek": "Uylar katta"},
    {"level_id": 4, "topic_id": 5, "arabic_word": "مَدَارِسُ", "uzbek_translation": "🏫 Maktablar", "transliteration": "madaarisu", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 5 — Mavzu 3: Ta'om va ichimlik (7 ta)
    # ══════════════════════════════════════════════════════════════
    {"level_id": 5, "topic_id": 3, "arabic_word": "أَرُزٌّ", "uzbek_translation": "🍚 Guruch", "transliteration": "aruzzun", "category": "soz"},
    {"level_id": 5, "topic_id": 3, "arabic_word": "شَايٌ", "uzbek_translation": "🍵 Choy", "transliteration": "shaayun", "category": "soz",
     "example_sentence_arabic": "الشَّايُ حَارٌّ", "example_sentence_uzbek": "Choy issiq"},
    {"level_id": 5, "topic_id": 3, "arabic_word": "قَهْوَةٌ", "uzbek_translation": "☕ Qahva", "transliteration": "qahwatun", "category": "soz"},
    {"level_id": 5, "topic_id": 3, "arabic_word": "بَيْضٌ", "uzbek_translation": "🥚 Tuxum", "transliteration": "baydun", "category": "soz"},
    {"level_id": 5, "topic_id": 3, "arabic_word": "لَحْمٌ", "uzbek_translation": "🥩 Go'sht", "transliteration": "lahmun", "category": "soz",
     "example_sentence_arabic": "اللَّحْمُ لَذِيذٌ", "example_sentence_uzbek": "Go'sht mazali"},
    {"level_id": 5, "topic_id": 3, "arabic_word": "خُضَارٌ", "uzbek_translation": "🥦 Sabzavot", "transliteration": "khudaarun", "category": "soz"},
    {"level_id": 5, "topic_id": 3, "arabic_word": "فَاكِهَةٌ", "uzbek_translation": "🍎 Meva", "transliteration": "faakihatun", "category": "soz"},

    # MODULE 5 — Mavzu 4: Transport va yo'l (7 ta)
    {"level_id": 5, "topic_id": 4, "arabic_word": "سَيَّارَةٌ", "uzbek_translation": "🚗 Mashina", "transliteration": "sayyaaratun", "category": "soz",
     "example_sentence_arabic": "هَذِهِ سَيَّارَةٌ جَدِيدَةٌ", "example_sentence_uzbek": "Bu yangi mashina"},
    {"level_id": 5, "topic_id": 4, "arabic_word": "حَافِلَةٌ", "uzbek_translation": "🚌 Avtobus", "transliteration": "haafilatun", "category": "soz"},
    {"level_id": 5, "topic_id": 4, "arabic_word": "قِطَارٌ", "uzbek_translation": "🚂 Poyezd", "transliteration": "qitaarun", "category": "soz"},
    {"level_id": 5, "topic_id": 4, "arabic_word": "طَيَّارَةٌ", "uzbek_translation": "✈️ Samolyot", "transliteration": "tayyaaratun", "category": "soz"},
    {"level_id": 5, "topic_id": 4, "arabic_word": "شَارِعٌ", "uzbek_translation": "🛣️ Ko'cha", "transliteration": "shaari'un", "category": "soz"},
    {"level_id": 5, "topic_id": 4, "arabic_word": "مَحَطَّةٌ", "uzbek_translation": "🚏 Bekat", "transliteration": "mahatttatun", "category": "soz"},
    {"level_id": 5, "topic_id": 4, "arabic_word": "مَطَارٌ", "uzbek_translation": "✈️ Aeroport", "transliteration": "mataarun", "category": "soz",
     "example_sentence_arabic": "ذَهَبَ إِلَى الْمَطَارِ", "example_sentence_uzbek": "U aeroportga ketdi"},

    # MODULE 5 — Mavzu 5: Shahar va joylar (7 ta)
    {"level_id": 5, "topic_id": 5, "arabic_word": "سُوقٌ", "uzbek_translation": "🛒 Bozor", "transliteration": "sooqun", "category": "soz"},
    {"level_id": 5, "topic_id": 5, "arabic_word": "مَطْعَمٌ", "uzbek_translation": "🍽️ Restoran", "transliteration": "mat'amun", "category": "soz",
     "example_sentence_arabic": "الْمَطْعَمُ قَرِيبٌ", "example_sentence_uzbek": "Restoran yaqin"},
    {"level_id": 5, "topic_id": 5, "arabic_word": "فُنْدُقٌ", "uzbek_translation": "🏨 Mehmonxona", "transliteration": "funduqun", "category": "soz"},
    {"level_id": 5, "topic_id": 5, "arabic_word": "مُسْتَشْفَى", "uzbek_translation": "🏥 Kasalxona", "transliteration": "mustashfaa", "category": "soz"},
    {"level_id": 5, "topic_id": 5, "arabic_word": "مَكْتَبَةٌ", "uzbek_translation": "📖 Kutubxona", "transliteration": "maktabatun", "category": "soz",
     "example_sentence_arabic": "الْمَكْتَبَةُ بَعِيدَةٌ", "example_sentence_uzbek": "Kutubxona uzoq"},
    {"level_id": 5, "topic_id": 5, "arabic_word": "حَدِيقَةٌ", "uzbek_translation": "🌳 Bog' / Park", "transliteration": "hadeeqatun", "category": "soz"},
    {"level_id": 5, "topic_id": 5, "arabic_word": "مَكْتَبٌ", "uzbek_translation": "🏢 Ofis", "transliteration": "maktabun", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 6 — Mavzu 3: Vaqt iboralari (7 ta)
    # ══════════════════════════════════════════════════════════════
    {"level_id": 6, "topic_id": 3, "arabic_word": "يَوْمٌ", "uzbek_translation": "📅 Kun", "transliteration": "yawmun", "category": "soz",
     "example_sentence_arabic": "هَذَا يَوْمٌ جَمِيلٌ", "example_sentence_uzbek": "Bu chiroyli kun"},
    {"level_id": 6, "topic_id": 3, "arabic_word": "أُسْبُوعٌ", "uzbek_translation": "📆 Hafta", "transliteration": "usboo'un", "category": "soz"},
    {"level_id": 6, "topic_id": 3, "arabic_word": "شَهْرٌ", "uzbek_translation": "🗓️ Oy (vaqt)", "transliteration": "shahrun", "category": "soz"},
    {"level_id": 6, "topic_id": 3, "arabic_word": "سَنَةٌ", "uzbek_translation": "📅 Yil", "transliteration": "sanatun", "category": "soz"},
    {"level_id": 6, "topic_id": 3, "arabic_word": "صَبَاحٌ", "uzbek_translation": "🌅 Ertalab", "transliteration": "sabaahun", "category": "soz",
     "example_sentence_arabic": "أَذْهَبُ إِلَى الْمَدْرَسَةِ صَبَاحًا", "example_sentence_uzbek": "Men ertalab maktabga boraman"},
    {"level_id": 6, "topic_id": 3, "arabic_word": "مَسَاءٌ", "uzbek_translation": "🌆 Kechqurun", "transliteration": "masaa'un", "category": "soz"},
    {"level_id": 6, "topic_id": 3, "arabic_word": "لَيْلَةٌ", "uzbek_translation": "🌙 Kecha (tun)", "transliteration": "laylatun", "category": "soz"},

    # MODULE 6 — Mavzu 4: Bozor va xarid (7 ta)
    {"level_id": 6, "topic_id": 4, "arabic_word": "ثَمَنٌ", "uzbek_translation": "💰 Narx", "transliteration": "thamanun", "category": "soz",
     "example_sentence_arabic": "مَا ثَمَنُ هَذَا؟", "example_sentence_uzbek": "Buning narxi necha?"},
    {"level_id": 6, "topic_id": 4, "arabic_word": "نُقُودٌ", "uzbek_translation": "💵 Pul", "transliteration": "nuqoodun", "category": "soz"},
    {"level_id": 6, "topic_id": 4, "arabic_word": "بَائِعٌ", "uzbek_translation": "🛍️ Sotuvchi", "transliteration": "baa'i'un", "category": "soz"},
    {"level_id": 6, "topic_id": 4, "arabic_word": "خَصْمٌ", "uzbek_translation": "🏷️ Chegirma", "transliteration": "khasmun", "category": "soz"},
    {"level_id": 6, "topic_id": 4, "arabic_word": "كَثِيرٌ", "uzbek_translation": "➕ Ko'p", "transliteration": "katheerun", "category": "soz",
     "example_sentence_arabic": "عِنْدِي نُقُودٌ كَثِيرَةٌ", "example_sentence_uzbek": "Menda ko'p pul bor"},
    {"level_id": 6, "topic_id": 4, "arabic_word": "قَلِيلٌ", "uzbek_translation": "➖ Oz / Kam", "transliteration": "qaleelun", "category": "soz"},
    {"level_id": 6, "topic_id": 4, "arabic_word": "مَحَلٌّ", "uzbek_translation": "🏪 Magazin", "transliteration": "mahallun", "category": "soz"},

    # MODULE 6 — Mavzu 5: Sog'liq (7 ta)
    {"level_id": 6, "topic_id": 5, "arabic_word": "دَوَاءٌ", "uzbek_translation": "💊 Dori", "transliteration": "dawaa'un", "category": "soz"},
    {"level_id": 6, "topic_id": 5, "arabic_word": "أَلَمٌ", "uzbek_translation": "😣 Og'riq", "transliteration": "alamun", "category": "soz",
     "example_sentence_arabic": "عِنْدِي أَلَمٌ فِي الرَّأْسِ", "example_sentence_uzbek": "Mening boshim og'riydi"},
    {"level_id": 6, "topic_id": 5, "arabic_word": "مَرَضٌ", "uzbek_translation": "🤒 Kasallik", "transliteration": "maradun", "category": "soz"},
    {"level_id": 6, "topic_id": 5, "arabic_word": "صَيْدَلِيَّةٌ", "uzbek_translation": "💊 Dorixona", "transliteration": "saydaliyyatun", "category": "soz"},
    {"level_id": 6, "topic_id": 5, "arabic_word": "سُخُونَةٌ", "uzbek_translation": "🌡️ Isitma", "transliteration": "sukhoonatun", "category": "soz"},
    {"level_id": 6, "topic_id": 5, "arabic_word": "صُدَاعٌ", "uzbek_translation": "🤕 Bosh og'rig'i", "transliteration": "sudaa'un", "category": "soz"},
    {"level_id": 6, "topic_id": 5, "arabic_word": "عِلَاجٌ", "uzbek_translation": "🩺 Davolash", "transliteration": "'ilaajun", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 7 — Mavzu 3: Millatlar (7 ta)
    # ══════════════════════════════════════════════════════════════
    {"level_id": 7, "topic_id": 3, "arabic_word": "عَرَبِيٌّ", "uzbek_translation": "🇸🇦 Arab", "transliteration": "arabiyyun", "category": "soz",
     "example_sentence_arabic": "هُوَ عَرَبِيٌّ", "example_sentence_uzbek": "U arab"},
    {"level_id": 7, "topic_id": 3, "arabic_word": "إِنْجِلِيزِيٌّ", "uzbek_translation": "🇬🇧 Ingliz", "transliteration": "injileeziyyun", "category": "soz"},
    {"level_id": 7, "topic_id": 3, "arabic_word": "فَرَنْسِيٌّ", "uzbek_translation": "🇫🇷 Fransuz", "transliteration": "faransiyyun", "category": "soz"},
    {"level_id": 7, "topic_id": 3, "arabic_word": "صِينِيٌّ", "uzbek_translation": "🇨🇳 Xitoy", "transliteration": "seeniyyun", "category": "soz"},
    {"level_id": 7, "topic_id": 3, "arabic_word": "هِنْدِيٌّ", "uzbek_translation": "🇮🇳 Hind", "transliteration": "hindiyyun", "category": "soz"},
    {"level_id": 7, "topic_id": 3, "arabic_word": "تُرْكِيٌّ", "uzbek_translation": "🇹🇷 Turk", "transliteration": "turkiyyun", "category": "soz"},
    {"level_id": 7, "topic_id": 3, "arabic_word": "أَجْنَبِيٌّ", "uzbek_translation": "🌍 Xorijiy", "transliteration": "ajnabiyyun", "category": "soz"},

    # MODULE 7 — Mavzu 4: Ravishlar (7 ta)
    {"level_id": 7, "topic_id": 4, "arabic_word": "جِدًّا", "uzbek_translation": "‼️ Juda", "transliteration": "jiddan", "category": "zamir",
     "example_sentence_arabic": "هُوَ طَالِبٌ جَيِّدٌ جِدًّا", "example_sentence_uzbek": "U juda yaxshi talaba"},
    {"level_id": 7, "topic_id": 4, "arabic_word": "أَيْضًا", "uzbek_translation": "➕ Ham / Shuningdek", "transliteration": "aydan", "category": "zamir"},
    {"level_id": 7, "topic_id": 4, "arabic_word": "فَقَطْ", "uzbek_translation": "🔹 Faqat", "transliteration": "faqat", "category": "zamir"},
    {"level_id": 7, "topic_id": 4, "arabic_word": "دَائِمًا", "uzbek_translation": "🔄 Doim", "transliteration": "daa'iman", "category": "zamir"},
    {"level_id": 7, "topic_id": 4, "arabic_word": "أَحْيَانًا", "uzbek_translation": "🔁 Ba'zan", "transliteration": "ahyaanan", "category": "zamir"},
    {"level_id": 7, "topic_id": 4, "arabic_word": "أَبَدًا", "uzbek_translation": "❌ Hech qachon", "transliteration": "abadan", "category": "zamir"},
    {"level_id": 7, "topic_id": 4, "arabic_word": "الْآنَ", "uzbek_translation": "⏱️ Hozir", "transliteration": "al-aana", "category": "zamir",
     "example_sentence_arabic": "أَنَا هُنَا الْآنَ", "example_sentence_uzbek": "Men hozir bu yerdaman"},

    # MODULE 7 — Mavzu 5: Bog'lovchilar (7 ta)
    {"level_id": 7, "topic_id": 5, "arabic_word": "وَ", "uzbek_translation": "➕ Va", "transliteration": "wa", "category": "zamir"},
    {"level_id": 7, "topic_id": 5, "arabic_word": "أَوْ", "uzbek_translation": "🔀 Yoki", "transliteration": "aw", "category": "zamir"},
    {"level_id": 7, "topic_id": 5, "arabic_word": "لَكِنْ", "uzbek_translation": "↩️ Lekin", "transliteration": "laakin", "category": "zamir",
     "example_sentence_arabic": "هُوَ كَبِيرٌ لَكِنَّهُ طَيِّبٌ", "example_sentence_uzbek": "U katta, lekin yaxshi"},
    {"level_id": 7, "topic_id": 5, "arabic_word": "لِأَنَّ", "uzbek_translation": "🔍 Chunki", "transliteration": "li'anna", "category": "zamir"},
    {"level_id": 7, "topic_id": 5, "arabic_word": "إِذَا", "uzbek_translation": "❓ Agar", "transliteration": "izaa", "category": "zamir"},
    {"level_id": 7, "topic_id": 5, "arabic_word": "عِنْدَمَا", "uzbek_translation": "🕐 Qachonki", "transliteration": "'indamaa", "category": "zamir"},
    {"level_id": 7, "topic_id": 5, "arabic_word": "ثُمَّ", "uzbek_translation": "➡️ Keyin / So'ng", "transliteration": "thumma", "category": "zamir"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 8 — Mavzu 3: Taqqoslash sifatlari (7 ta)
    # ══════════════════════════════════════════════════════════════
    {"level_id": 8, "topic_id": 3, "arabic_word": "أَكْبَرُ", "uzbek_translation": "🔼 Kattaroq", "transliteration": "akbaru", "category": "sifat",
     "example_sentence_arabic": "هَذَا الْبَيْتُ أَكْبَرُ", "example_sentence_uzbek": "Bu uy kattaroq"},
    {"level_id": 8, "topic_id": 3, "arabic_word": "أَصْغَرُ", "uzbek_translation": "🔽 Kichikroq", "transliteration": "asgharu", "category": "sifat"},
    {"level_id": 8, "topic_id": 3, "arabic_word": "أَحْسَنُ", "uzbek_translation": "✅ Yaxshiroq", "transliteration": "ahsanu", "category": "sifat"},
    {"level_id": 8, "topic_id": 3, "arabic_word": "أَكْثَرُ", "uzbek_translation": "➕ Ko'proq", "transliteration": "aktharu", "category": "sifat"},
    {"level_id": 8, "topic_id": 3, "arabic_word": "أَقَلُّ", "uzbek_translation": "➖ Kamroq", "transliteration": "aqallu", "category": "sifat"},
    {"level_id": 8, "topic_id": 3, "arabic_word": "أَطْوَلُ", "uzbek_translation": "📏 Uzunroq / Balandroq", "transliteration": "atwalu", "category": "sifat"},
    {"level_id": 8, "topic_id": 3, "arabic_word": "أَسْرَعُ", "uzbek_translation": "⚡ Tezroq", "transliteration": "asra'u", "category": "sifat",
     "example_sentence_arabic": "الطَّيَّارَةُ أَسْرَعُ مِنَ السَّيَّارَةِ", "example_sentence_uzbek": "Samolyot mashinadan tezroq"},

    # MODULE 8 — Mavzu 4: His-tuyg'ular (7 ta)
    {"level_id": 8, "topic_id": 4, "arabic_word": "سَعِيدٌ", "uzbek_translation": "😊 Xursand", "transliteration": "sa'eedun", "category": "sifat",
     "example_sentence_arabic": "أَنَا سَعِيدٌ الْيَوْمَ", "example_sentence_uzbek": "Men bugun xursandman"},
    {"level_id": 8, "topic_id": 4, "arabic_word": "حَزِينٌ", "uzbek_translation": "😢 Xafa / G'amgin", "transliteration": "hazeenun", "category": "sifat"},
    {"level_id": 8, "topic_id": 4, "arabic_word": "غَاضِبٌ", "uzbek_translation": "😠 G'azablangan", "transliteration": "ghaadibun", "category": "sifat"},
    {"level_id": 8, "topic_id": 4, "arabic_word": "خَائِفٌ", "uzbek_translation": "😨 Qo'rqgan", "transliteration": "khaa'ifun", "category": "sifat"},
    {"level_id": 8, "topic_id": 4, "arabic_word": "مُتَعَجِّبٌ", "uzbek_translation": "😮 Hayron", "transliteration": "muta'ajjibun", "category": "sifat"},
    {"level_id": 8, "topic_id": 4, "arabic_word": "مُتْعَبٌ", "uzbek_translation": "😴 Charchagan", "transliteration": "mut'abun", "category": "sifat"},
    {"level_id": 8, "topic_id": 4, "arabic_word": "نَشِيطٌ", "uzbek_translation": "💪 Faol / Energik", "transliteration": "nasheitun", "category": "sifat"},

    # MODULE 8 — Mavzu 5: Muhim sifatlar (7 ta)
    {"level_id": 8, "topic_id": 5, "arabic_word": "صَحِيحٌ", "uzbek_translation": "✅ To'g'ri", "transliteration": "saheehun", "category": "sifat",
     "example_sentence_arabic": "هَذَا الْجَوَابُ صَحِيحٌ", "example_sentence_uzbek": "Bu javob to'g'ri"},
    {"level_id": 8, "topic_id": 5, "arabic_word": "خَاطِئٌ", "uzbek_translation": "❌ Noto'g'ri", "transliteration": "khaati'un", "category": "sifat"},
    {"level_id": 8, "topic_id": 5, "arabic_word": "مُمْكِنٌ", "uzbek_translation": "💡 Mumkin", "transliteration": "mumkinun", "category": "sifat"},
    {"level_id": 8, "topic_id": 5, "arabic_word": "صَعْبٌ", "uzbek_translation": "😤 Qiyin", "transliteration": "sa'bun", "category": "sifat",
     "example_sentence_arabic": "هَذَا الدَّرْسُ صَعْبٌ", "example_sentence_uzbek": "Bu dars qiyin"},
    {"level_id": 8, "topic_id": 5, "arabic_word": "سَهْلٌ", "uzbek_translation": "😊 Oson", "transliteration": "sahlun", "category": "sifat"},
    {"level_id": 8, "topic_id": 5, "arabic_word": "مُهِمٌّ", "uzbek_translation": "❗ Muhim", "transliteration": "muhimmun", "category": "sifat"},
    {"level_id": 8, "topic_id": 5, "arabic_word": "مُمْتِعٌ", "uzbek_translation": "🎉 Qiziqarli", "transliteration": "mumti'un", "category": "sifat"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 9 — Mavzu 3: Muzori' fe'llari (hozirgi zamon) (7 ta)
    # ══════════════════════════════════════════════════════════════
    {"level_id": 9, "topic_id": 3, "arabic_word": "يَكْتُبُ", "uzbek_translation": "✍️ Yozmoqda", "transliteration": "yaktubu", "category": "fel",
     "example_sentence_arabic": "الطَّالِبُ يَكْتُبُ الدَّرْسَ", "example_sentence_uzbek": "Talaba darsni yozmoqda"},
    {"level_id": 9, "topic_id": 3, "arabic_word": "يَقْرَأُ", "uzbek_translation": "📖 O'qimoqda", "transliteration": "yaqra'u", "category": "fel"},
    {"level_id": 9, "topic_id": 3, "arabic_word": "يَذْهَبُ", "uzbek_translation": "🚶 Ketmoqda", "transliteration": "yazhabu", "category": "fel",
     "example_sentence_arabic": "هُوَ يَذْهَبُ إِلَى الْمَدْرَسَةِ", "example_sentence_uzbek": "U maktabga ketmoqda"},
    {"level_id": 9, "topic_id": 3, "arabic_word": "يَأْكُلُ", "uzbek_translation": "🍽️ Yemoqda", "transliteration": "ya'kulu", "category": "fel"},
    {"level_id": 9, "topic_id": 3, "arabic_word": "يَشْرَبُ", "uzbek_translation": "🥤 Ichmoqda", "transliteration": "yashrabu", "category": "fel"},
    {"level_id": 9, "topic_id": 3, "arabic_word": "يَنَامُ", "uzbek_translation": "😴 Uxlamoqda", "transliteration": "yanaamu", "category": "fel"},
    {"level_id": 9, "topic_id": 3, "arabic_word": "يَتَكَلَّمُ", "uzbek_translation": "🗣️ Gapirmoqda", "transliteration": "yatakallamu", "category": "fel",
     "example_sentence_arabic": "هُوَ يَتَكَلَّمُ بِالْعَرَبِيَّةِ", "example_sentence_uzbek": "U arabcha gapirmoqda"},

    # MODULE 9 — Mavzu 4: Amr fe'llari (7 ta)
    {"level_id": 9, "topic_id": 4, "arabic_word": "اكْتُبْ", "uzbek_translation": "✍️ Yoz!", "transliteration": "uktub", "category": "fel",
     "example_sentence_arabic": "اكْتُبْ دَرْسَكَ", "example_sentence_uzbek": "Darsингni yoz!"},
    {"level_id": 9, "topic_id": 4, "arabic_word": "اقْرَأْ", "uzbek_translation": "📖 O'qi!", "transliteration": "iqra'", "category": "fel"},
    {"level_id": 9, "topic_id": 4, "arabic_word": "اذْهَبْ", "uzbek_translation": "🚶 Ket!", "transliteration": "izhhab", "category": "fel"},
    {"level_id": 9, "topic_id": 4, "arabic_word": "تَعَالَ", "uzbek_translation": "👋 Kel!", "transliteration": "ta'aal", "category": "fel",
     "example_sentence_arabic": "تَعَالَ إِلَى هُنَا", "example_sentence_uzbek": "Bu yerga kel!"},
    {"level_id": 9, "topic_id": 4, "arabic_word": "انْظُرْ", "uzbek_translation": "👀 Qara!", "transliteration": "unzur", "category": "fel"},
    {"level_id": 9, "topic_id": 4, "arabic_word": "اجْلِسْ", "uzbek_translation": "🪑 O'tir!", "transliteration": "ijlis", "category": "fel"},
    {"level_id": 9, "topic_id": 4, "arabic_word": "قِفْ", "uzbek_translation": "🛑 To'xta!", "transliteration": "qif", "category": "fel"},

    # MODULE 9 — Mavzu 5: Kundalik hayot fe'llari (7 ta)
    {"level_id": 9, "topic_id": 5, "arabic_word": "اسْتَيْقَظَ", "uzbek_translation": "⏰ Uyg'andi", "transliteration": "istayqaza", "category": "fel",
     "example_sentence_arabic": "اسْتَيْقَظَ مُبَكِّرًا", "example_sentence_uzbek": "U erta uyg'andi"},
    {"level_id": 9, "topic_id": 5, "arabic_word": "تَنَاوَلَ", "uzbek_translation": "🍽️ Ovqatlandi", "transliteration": "tanaawala", "category": "fel"},
    {"level_id": 9, "topic_id": 5, "arabic_word": "طَبَخَ", "uzbek_translation": "🍳 Pishirdi", "transliteration": "tabakha", "category": "fel"},
    {"level_id": 9, "topic_id": 5, "arabic_word": "نَظَّفَ", "uzbek_translation": "🧹 Tozaladi", "transliteration": "nazzafa", "category": "fel",
     "example_sentence_arabic": "نَظَّفَ الْغُرْفَةَ", "example_sentence_uzbek": "Xonani tozaladi"},
    {"level_id": 9, "topic_id": 5, "arabic_word": "سَاعَدَ", "uzbek_translation": "🤝 Yordam berdi", "transliteration": "saa'ada", "category": "fel"},
    {"level_id": 9, "topic_id": 5, "arabic_word": "تَعَلَّمَ", "uzbek_translation": "📚 O'rgandi", "transliteration": "ta'allama", "category": "fel"},
    {"level_id": 9, "topic_id": 5, "arabic_word": "حَفِظَ", "uzbek_translation": "🧠 Yod oldi", "transliteration": "hafiza", "category": "fel",
     "example_sentence_arabic": "حَفِظَ الدَّرْسَ جَيِّدًا", "example_sentence_uzbek": "Darsni yaxshi yod oldi"},

    # ══════════════════════════════════════════════════════════════
    # MODULE 10 — Mavzu 3: Harf jarr (predloglar) (7 ta)
    # ══════════════════════════════════════════════════════════════
    {"level_id": 10, "topic_id": 3, "arabic_word": "فِي", "uzbek_translation": "📍 ...da / ...ichida", "transliteration": "fee", "category": "fel",
     "example_sentence_arabic": "الْكِتَابُ فِي الْحَقِيبَةِ", "example_sentence_uzbek": "Kitob sumkada"},
    {"level_id": 10, "topic_id": 3, "arabic_word": "إِلَى", "uzbek_translation": "➡️ ...ga / tomon", "transliteration": "ilaa", "category": "fel"},
    {"level_id": 10, "topic_id": 3, "arabic_word": "مِنْ", "uzbek_translation": "⬅️ ...dan", "transliteration": "min", "category": "fel",
     "example_sentence_arabic": "جَاءَ مِنَ الْبَيْتِ", "example_sentence_uzbek": "Uydan keldi"},
    {"level_id": 10, "topic_id": 3, "arabic_word": "عَلَى", "uzbek_translation": "⬆️ ...ustida / ...da", "transliteration": "alaa", "category": "fel"},
    {"level_id": 10, "topic_id": 3, "arabic_word": "عَنْ", "uzbek_translation": "💬 ...haqida / ...dan", "transliteration": "an", "category": "fel"},
    {"level_id": 10, "topic_id": 3, "arabic_word": "مَعَ", "uzbek_translation": "🤝 ...bilan", "transliteration": "ma'a", "category": "fel"},
    {"level_id": 10, "topic_id": 3, "arabic_word": "بَيْنَ", "uzbek_translation": "↔️ ...orasida", "transliteration": "bayna", "category": "fel",
     "example_sentence_arabic": "الْكِتَابُ بَيْنَ الْقَلَمَيْنِ", "example_sentence_uzbek": "Kitob ikki qalam orasida"},

    # MODULE 10 — Mavzu 4: Makonga oid zarflar (7 ta)
    {"level_id": 10, "topic_id": 4, "arabic_word": "بَعْدَ", "uzbek_translation": "⏭️ ...dan keyin", "transliteration": "ba'da", "category": "fel",
     "example_sentence_arabic": "جَاءَ بَعْدَ الدَّرْسِ", "example_sentence_uzbek": "Darsdan keyin keldi"},
    {"level_id": 10, "topic_id": 4, "arabic_word": "قَبْلَ", "uzbek_translation": "⏮️ ...dan oldin", "transliteration": "qabla", "category": "fel"},
    {"level_id": 10, "topic_id": 4, "arabic_word": "فَوْقَ", "uzbek_translation": "⬆️ Ustida", "transliteration": "fawqa", "category": "fel"},
    {"level_id": 10, "topic_id": 4, "arabic_word": "تَحْتَ", "uzbek_translation": "⬇️ Ostida", "transliteration": "tahta", "category": "fel",
     "example_sentence_arabic": "الْكِتَابُ تَحْتَ الطَّاوِلَةِ", "example_sentence_uzbek": "Kitob stol ostida"},
    {"level_id": 10, "topic_id": 4, "arabic_word": "أَمَامَ", "uzbek_translation": "⬆️ Oldida", "transliteration": "amaama", "category": "fel"},
    {"level_id": 10, "topic_id": 4, "arabic_word": "خَلْفَ", "uzbek_translation": "↩️ Ortida", "transliteration": "khalfa", "category": "fel"},
    {"level_id": 10, "topic_id": 4, "arabic_word": "بِجَانِبِ", "uzbek_translation": "↔️ Yonida", "transliteration": "bijaanibi", "category": "fel"},

    # MODULE 10 — Mavzu 5: Aloqa fe'llari 2 (7 ta)
    {"level_id": 10, "topic_id": 5, "arabic_word": "قَرَّرَ", "uzbek_translation": "✅ Qaror qildi", "transliteration": "qarrara", "category": "fel",
     "example_sentence_arabic": "قَرَّرَ السَّفَرَ غَدًا", "example_sentence_uzbek": "Ertaga safar qilishga qaror qildi"},
    {"level_id": 10, "topic_id": 5, "arabic_word": "نَجَحَ", "uzbek_translation": "🏆 Muvaffaq bo'ldi", "transliteration": "najaha", "category": "fel"},
    {"level_id": 10, "topic_id": 5, "arabic_word": "فَشِلَ", "uzbek_translation": "❌ Muvaffaqiyatsiz bo'ldi", "transliteration": "fashila", "category": "fel"},
    {"level_id": 10, "topic_id": 5, "arabic_word": "حَاوَلَ", "uzbek_translation": "💪 Urindi / Harakat qildi", "transliteration": "haawala", "category": "fel",
     "example_sentence_arabic": "حَاوَلَ كَثِيرًا", "example_sentence_uzbek": "Ko'p harakat qildi"},
    {"level_id": 10, "topic_id": 5, "arabic_word": "تَذَكَّرَ", "uzbek_translation": "🧠 Esladi", "transliteration": "tazakkara", "category": "fel"},
    {"level_id": 10, "topic_id": 5, "arabic_word": "نَسِيَ", "uzbek_translation": "😶 Unutdi", "transliteration": "nasiya", "category": "fel"},
    {"level_id": 10, "topic_id": 5, "arabic_word": "انْتَظَرَ", "uzbek_translation": "⏳ Kutdi", "transliteration": "intazara", "category": "fel",
     "example_sentence_arabic": "انْتَظَرَ طَوِيلًا", "example_sentence_uzbek": "Uzoq kutdi"},
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
