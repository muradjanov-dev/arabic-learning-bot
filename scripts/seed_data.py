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
    # LEVEL 1 — Alifbo (1): ا ب ت ث ج ح خ
    # ══════════════════════════════════════════════════════════════
    {"level_id": 1, "arabic_word": "ا", "uzbek_translation": "Alif", "transliteration": "alif", "category": "harf"},
    {"level_id": 1, "arabic_word": "ب", "uzbek_translation": "Ba", "transliteration": "ba", "category": "harf"},
    {"level_id": 1, "arabic_word": "ت", "uzbek_translation": "Ta", "transliteration": "ta", "category": "harf"},
    {"level_id": 1, "arabic_word": "ث", "uzbek_translation": "Sa", "transliteration": "sa", "category": "harf"},
    {"level_id": 1, "arabic_word": "ج", "uzbek_translation": "Jim", "transliteration": "jim", "category": "harf"},
    {"level_id": 1, "arabic_word": "ح", "uzbek_translation": "Ha", "transliteration": "ha", "category": "harf"},
    {"level_id": 1, "arabic_word": "خ", "uzbek_translation": "Xa", "transliteration": "kha", "category": "harf"},
    {"level_id": 1, "arabic_word": "بَابٌ", "uzbek_translation": "Eshik", "transliteration": "baab", "category": "soz",
     "example_sentence_arabic": "هَذَا بَابٌ كَبِيرٌ", "example_sentence_uzbek": "Bu katta eshik"},
    {"level_id": 1, "arabic_word": "تَمْرٌ", "uzbek_translation": "Xurmo", "transliteration": "tamr", "category": "soz"},
    {"level_id": 1, "arabic_word": "جَبَلٌ", "uzbek_translation": "Tog'", "transliteration": "jabal", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # LEVEL 2 — Alifbo (2): د ذ ر ز س ش ص
    # ══════════════════════════════════════════════════════════════
    {"level_id": 2, "arabic_word": "د", "uzbek_translation": "Dal", "transliteration": "dal", "category": "harf"},
    {"level_id": 2, "arabic_word": "ذ", "uzbek_translation": "Zal", "transliteration": "zal", "category": "harf"},
    {"level_id": 2, "arabic_word": "ر", "uzbek_translation": "Ra", "transliteration": "ra", "category": "harf"},
    {"level_id": 2, "arabic_word": "ز", "uzbek_translation": "Zay", "transliteration": "zay", "category": "harf"},
    {"level_id": 2, "arabic_word": "س", "uzbek_translation": "Sin", "transliteration": "sin", "category": "harf"},
    {"level_id": 2, "arabic_word": "ش", "uzbek_translation": "Shin", "transliteration": "shin", "category": "harf"},
    {"level_id": 2, "arabic_word": "ص", "uzbek_translation": "Sod", "transliteration": "sad", "category": "harf"},
    {"level_id": 2, "arabic_word": "دَارٌ", "uzbek_translation": "Uy", "transliteration": "daar", "category": "soz",
     "example_sentence_arabic": "هَذِهِ دَارٌ", "example_sentence_uzbek": "Bu uy"},
    {"level_id": 2, "arabic_word": "رَأْسٌ", "uzbek_translation": "Bosh", "transliteration": "ra's", "category": "soz"},
    {"level_id": 2, "arabic_word": "سَمَكٌ", "uzbek_translation": "Baliq", "transliteration": "samak", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # LEVEL 3 — Alifbo (3): ض ط ظ ع غ ف ق
    # ══════════════════════════════════════════════════════════════
    {"level_id": 3, "arabic_word": "ض", "uzbek_translation": "Zod", "transliteration": "dad", "category": "harf"},
    {"level_id": 3, "arabic_word": "ط", "uzbek_translation": "To", "transliteration": "ta", "category": "harf"},
    {"level_id": 3, "arabic_word": "ظ", "uzbek_translation": "Zo", "transliteration": "za", "category": "harf"},
    {"level_id": 3, "arabic_word": "ع", "uzbek_translation": "Ayn", "transliteration": "ain", "category": "harf"},
    {"level_id": 3, "arabic_word": "غ", "uzbek_translation": "G'ayn", "transliteration": "ghain", "category": "harf"},
    {"level_id": 3, "arabic_word": "ف", "uzbek_translation": "Fa", "transliteration": "fa", "category": "harf"},
    {"level_id": 3, "arabic_word": "ق", "uzbek_translation": "Qof", "transliteration": "qaf", "category": "harf"},
    {"level_id": 3, "arabic_word": "طَيْرٌ", "uzbek_translation": "Qush", "transliteration": "tayr", "category": "soz"},
    {"level_id": 3, "arabic_word": "عَيْنٌ", "uzbek_translation": "Ko'z", "transliteration": "ayn", "category": "soz"},
    {"level_id": 3, "arabic_word": "قَمَرٌ", "uzbek_translation": "Oy", "transliteration": "qamar", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # LEVEL 4 — Alifbo (4): ك ل م ن و ه ي
    # ══════════════════════════════════════════════════════════════
    {"level_id": 4, "arabic_word": "ك", "uzbek_translation": "Kof", "transliteration": "kaf", "category": "harf"},
    {"level_id": 4, "arabic_word": "ل", "uzbek_translation": "Lom", "transliteration": "lam", "category": "harf"},
    {"level_id": 4, "arabic_word": "م", "uzbek_translation": "Mim", "transliteration": "mim", "category": "harf"},
    {"level_id": 4, "arabic_word": "ن", "uzbek_translation": "Nun", "transliteration": "nun", "category": "harf"},
    {"level_id": 4, "arabic_word": "و", "uzbek_translation": "Vov", "transliteration": "waw", "category": "harf"},
    {"level_id": 4, "arabic_word": "ه", "uzbek_translation": "Ha (oxirgi)", "transliteration": "ha", "category": "harf"},
    {"level_id": 4, "arabic_word": "ي", "uzbek_translation": "Ya", "transliteration": "ya", "category": "harf"},
    {"level_id": 4, "arabic_word": "كَلْبٌ", "uzbek_translation": "It", "transliteration": "kalb", "category": "soz"},
    {"level_id": 4, "arabic_word": "لَيْلٌ", "uzbek_translation": "Kecha", "transliteration": "layl", "category": "soz"},
    {"level_id": 4, "arabic_word": "نَهْرٌ", "uzbek_translation": "Daryo", "transliteration": "nahr", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # LEVEL 5 — Harakatlar (unli belgilari)
    # ══════════════════════════════════════════════════════════════
    {"level_id": 5, "arabic_word": "َ", "uzbek_translation": "Fatha (a)", "transliteration": "fatha", "category": "harakat"},
    {"level_id": 5, "arabic_word": "ِ", "uzbek_translation": "Kasra (i)", "transliteration": "kasra", "category": "harakat"},
    {"level_id": 5, "arabic_word": "ُ", "uzbek_translation": "Damma (u)", "transliteration": "damma", "category": "harakat"},
    {"level_id": 5, "arabic_word": "ْ", "uzbek_translation": "Sukun (sokin)", "transliteration": "sukun", "category": "harakat"},
    {"level_id": 5, "arabic_word": "ً", "uzbek_translation": "Tanvin fatha (an)", "transliteration": "tanwin fatha", "category": "harakat"},
    {"level_id": 5, "arabic_word": "ٍ", "uzbek_translation": "Tanvin kasra (in)", "transliteration": "tanwin kasra", "category": "harakat"},
    {"level_id": 5, "arabic_word": "ٌ", "uzbek_translation": "Tanvin damma (un)", "transliteration": "tanwin damma", "category": "harakat"},
    {"level_id": 5, "arabic_word": "ّ", "uzbek_translation": "Shadda (ikkilanish)", "transliteration": "shadda", "category": "harakat"},
    {"level_id": 5, "arabic_word": "بَا", "uzbek_translation": "Ba + uzun a (madd alif)", "transliteration": "baa", "category": "harakat"},
    {"level_id": 5, "arabic_word": "بِي", "uzbek_translation": "Bi + uzun i (madd ya)", "transliteration": "bii", "category": "harakat"},

    # ══════════════════════════════════════════════════════════════
    # LEVEL 6 — Mabdaul Qiroat: Oddiy so'zlar (1)
    # ══════════════════════════════════════════════════════════════
    {"level_id": 6, "arabic_word": "كِتَابٌ", "uzbek_translation": "Kitob", "transliteration": "kitaab", "category": "soz",
     "example_sentence_arabic": "هَذَا كِتَابٌ جَدِيدٌ", "example_sentence_uzbek": "Bu yangi kitob"},
    {"level_id": 6, "arabic_word": "قَلَمٌ", "uzbek_translation": "Qalam", "transliteration": "qalam", "category": "soz",
     "example_sentence_arabic": "هَذَا قَلَمٌ أَحْمَرُ", "example_sentence_uzbek": "Bu qizil qalam"},
    {"level_id": 6, "arabic_word": "بَيْتٌ", "uzbek_translation": "Uy", "transliteration": "bayt", "category": "soz",
     "example_sentence_arabic": "هَذَا بَيْتٌ كَبِيرٌ", "example_sentence_uzbek": "Bu katta uy"},
    {"level_id": 6, "arabic_word": "شَجَرَةٌ", "uzbek_translation": "Daraxt", "transliteration": "shajara", "category": "soz"},
    {"level_id": 6, "arabic_word": "سَمَاءٌ", "uzbek_translation": "Osmon", "transliteration": "samaa", "category": "soz"},
    {"level_id": 6, "arabic_word": "أَرْضٌ", "uzbek_translation": "Er / Zamin", "transliteration": "ard", "category": "soz"},
    {"level_id": 6, "arabic_word": "مَاءٌ", "uzbek_translation": "Suv", "transliteration": "maa", "category": "soz"},
    {"level_id": 6, "arabic_word": "نَارٌ", "uzbek_translation": "Olov", "transliteration": "naar", "category": "soz"},
    {"level_id": 6, "arabic_word": "شَمْسٌ", "uzbek_translation": "Quyosh", "transliteration": "shams", "category": "soz"},
    {"level_id": 6, "arabic_word": "قِطٌّ", "uzbek_translation": "Mushuk", "transliteration": "qitt", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # LEVEL 7 — Mabdaul Qiroat: Oddiy so'zlar (2) + Salomlashish
    # ══════════════════════════════════════════════════════════════
    {"level_id": 7, "arabic_word": "مَرْحَبًا", "uzbek_translation": "Salom / Xush kelibsiz", "transliteration": "marhaban", "category": "salomlashish"},
    {"level_id": 7, "arabic_word": "أَهْلًا", "uzbek_translation": "Ahlan", "transliteration": "ahlan", "category": "salomlashish"},
    {"level_id": 7, "arabic_word": "صَبَاحُ الْخَيْرِ", "uzbek_translation": "Xayrli tong", "transliteration": "sabaah al-khayr", "category": "salomlashish"},
    {"level_id": 7, "arabic_word": "مَسَاءُ الْخَيْرِ", "uzbek_translation": "Xayrli kech", "transliteration": "masaa al-khayr", "category": "salomlashish"},
    {"level_id": 7, "arabic_word": "شُكْرًا", "uzbek_translation": "Rahmat", "transliteration": "shukran", "category": "salomlashish"},
    {"level_id": 7, "arabic_word": "عَفْوًا", "uzbek_translation": "Iltimos / Marhamat", "transliteration": "afwan", "category": "salomlashish"},
    {"level_id": 7, "arabic_word": "مَعَ السَّلَامَةِ", "uzbek_translation": "Xayr / Ko'rishguncha", "transliteration": "maa as-salaama", "category": "salomlashish"},
    {"level_id": 7, "arabic_word": "أُسْرَةٌ", "uzbek_translation": "Oila", "transliteration": "usra", "category": "soz"},
    {"level_id": 7, "arabic_word": "وَلَدٌ", "uzbek_translation": "Bola (o'g'il)", "transliteration": "walad", "category": "soz"},
    {"level_id": 7, "arabic_word": "بِنْتٌ", "uzbek_translation": "Qiz", "transliteration": "bint", "category": "soz"},

    # ══════════════════════════════════════════════════════════════
    # LEVEL 8 — Shifohiya: Olmoshlar va ko'rsatish olmoshlari
    # ══════════════════════════════════════════════════════════════
    {"level_id": 8, "arabic_word": "أَنَا", "uzbek_translation": "Men", "transliteration": "ana", "category": "zamir",
     "example_sentence_arabic": "أَنَا طَالِبٌ", "example_sentence_uzbek": "Men talabaman"},
    {"level_id": 8, "arabic_word": "أَنْتَ", "uzbek_translation": "Sen (erkak)", "transliteration": "anta", "category": "zamir",
     "example_sentence_arabic": "أَنْتَ طَالِبٌ", "example_sentence_uzbek": "Sen talabasan"},
    {"level_id": 8, "arabic_word": "أَنْتِ", "uzbek_translation": "Sen (ayol)", "transliteration": "anti", "category": "zamir"},
    {"level_id": 8, "arabic_word": "هُوَ", "uzbek_translation": "U (erkak)", "transliteration": "huwa", "category": "zamir"},
    {"level_id": 8, "arabic_word": "هِيَ", "uzbek_translation": "U (ayol)", "transliteration": "hiya", "category": "zamir"},
    {"level_id": 8, "arabic_word": "نَحْنُ", "uzbek_translation": "Biz", "transliteration": "nahnu", "category": "zamir"},
    {"level_id": 8, "arabic_word": "هُمْ", "uzbek_translation": "Ular (erkak)", "transliteration": "hum", "category": "zamir"},
    {"level_id": 8, "arabic_word": "هَذَا", "uzbek_translation": "Bu (erkak)", "transliteration": "haaza", "category": "zamir",
     "example_sentence_arabic": "هَذَا كِتَابٌ", "example_sentence_uzbek": "Bu kitob"},
    {"level_id": 8, "arabic_word": "هَذِهِ", "uzbek_translation": "Bu (ayol)", "transliteration": "haazihi", "category": "zamir"},
    {"level_id": 8, "arabic_word": "ذَلِكَ", "uzbek_translation": "U / Ul (uzoq)", "transliteration": "zaalika", "category": "zamir"},

    # ══════════════════════════════════════════════════════════════
    # LEVEL 9 — Shifohiya: Sifatlar
    # ══════════════════════════════════════════════════════════════
    {"level_id": 9, "arabic_word": "كَبِيرٌ", "uzbek_translation": "Katta", "transliteration": "kabiir", "category": "sifat",
     "example_sentence_arabic": "هَذَا بَيْتٌ كَبِيرٌ", "example_sentence_uzbek": "Bu katta uy"},
    {"level_id": 9, "arabic_word": "صَغِيرٌ", "uzbek_translation": "Kichik", "transliteration": "saghiir", "category": "sifat",
     "example_sentence_arabic": "هَذَا كِتَابٌ صَغِيرٌ", "example_sentence_uzbek": "Bu kichik kitob"},
    {"level_id": 9, "arabic_word": "جَدِيدٌ", "uzbek_translation": "Yangi", "transliteration": "jadiid", "category": "sifat"},
    {"level_id": 9, "arabic_word": "قَدِيمٌ", "uzbek_translation": "Eski", "transliteration": "qadiim", "category": "sifat"},
    {"level_id": 9, "arabic_word": "جَمِيلٌ", "uzbek_translation": "Chiroyli", "transliteration": "jamiil", "category": "sifat"},
    {"level_id": 9, "arabic_word": "سَرِيعٌ", "uzbek_translation": "Tez", "transliteration": "sarii", "category": "sifat"},
    {"level_id": 9, "arabic_word": "بَطِيءٌ", "uzbek_translation": "Sekin", "transliteration": "batii", "category": "sifat"},
    {"level_id": 9, "arabic_word": "طَوِيلٌ", "uzbek_translation": "Uzun / Baland", "transliteration": "tawiil", "category": "sifat"},
    {"level_id": 9, "arabic_word": "قَصِيرٌ", "uzbek_translation": "Qisqa / Past", "transliteration": "qasiir", "category": "sifat"},
    {"level_id": 9, "arabic_word": "قَوِيٌّ", "uzbek_translation": "Kuchli", "transliteration": "qawiyy", "category": "sifat"},

    # ══════════════════════════════════════════════════════════════
    # LEVEL 10 — Shifohiya: Fe'llar va jumlalar
    # ══════════════════════════════════════════════════════════════
    {"level_id": 10, "arabic_word": "ذَهَبَ", "uzbek_translation": "Ketdi", "transliteration": "zahaba", "category": "fel",
     "example_sentence_arabic": "ذَهَبَ الْوَلَدُ إِلَى الْبَيْتِ", "example_sentence_uzbek": "Bola uyga ketdi"},
    {"level_id": 10, "arabic_word": "جَاءَ", "uzbek_translation": "Keldi", "transliteration": "jaa'a", "category": "fel",
     "example_sentence_arabic": "جَاءَ الطَّالِبُ إِلَى الْفَصْلِ", "example_sentence_uzbek": "Talaba sinfga keldi"},
    {"level_id": 10, "arabic_word": "كَتَبَ", "uzbek_translation": "Yozdi", "transliteration": "kataba", "category": "fel",
     "example_sentence_arabic": "كَتَبَ الْوَلَدُ الدَّرْسَ", "example_sentence_uzbek": "Bola darsni yozdi"},
    {"level_id": 10, "arabic_word": "قَرَأَ", "uzbek_translation": "O'qidi", "transliteration": "qara'a", "category": "fel",
     "example_sentence_arabic": "قَرَأَ الطَّالِبُ الْكِتَابَ", "example_sentence_uzbek": "Talaba kitobni o'qidi"},
    {"level_id": 10, "arabic_word": "أَكَلَ", "uzbek_translation": "Yedi", "transliteration": "akala", "category": "fel"},
    {"level_id": 10, "arabic_word": "شَرِبَ", "uzbek_translation": "Ichdi", "transliteration": "shariba", "category": "fel"},
    {"level_id": 10, "arabic_word": "جَلَسَ", "uzbek_translation": "O'tirdi", "transliteration": "jalasa", "category": "fel"},
    {"level_id": 10, "arabic_word": "نَامَ", "uzbek_translation": "Uxladi", "transliteration": "naama", "category": "fel"},
    {"level_id": 10, "arabic_word": "فَتَحَ", "uzbek_translation": "Ochdi", "transliteration": "fataha", "category": "fel"},
    {"level_id": 10, "arabic_word": "دَخَلَ", "uzbek_translation": "Kirdi", "transliteration": "dakhala", "category": "fel",
     "example_sentence_arabic": "دَخَلَ الْوَلَدُ الْغُرْفَةَ", "example_sentence_uzbek": "Bola xonaga kirdi"},
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

    from sqlalchemy import delete
    async with async_session_maker() as session:
        # Wipe old religious content if present
        existing = (await session.execute(select(Vocabulary))).scalars().first()
        if existing:
            if existing.category in RELIGIOUS_CATEGORIES or existing.arabic_word in RELIGIOUS_WORDS:
                await session.execute(delete(Vocabulary))
                await session.commit()
                print("Wiped old religious vocabulary. Re-seeding...")
            else:
                print(f"Vocabulary already populated ({existing.word_id}+). Skipping.")
                return

        for item in VOCABULARY:
            session.add(Vocabulary(**item))
        await session.commit()
        print(f"Seeded {len(VOCABULARY)} vocabulary words across 10 levels.")


if __name__ == "__main__":
    asyncio.run(seed())
