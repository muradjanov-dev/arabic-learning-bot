"""
Run this script once after deployment to populate the vocabulary database.
Usage: python -m scripts.seed_data
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.database.base import engine, async_session_maker
from bot.database.models import Base, Vocabulary
from sqlalchemy import select

VOCABULARY = [
    # ─── Level 1: Gate of Sounds — Alphabet & Harakats ───────────────────────
    {"level_id": 1, "arabic_word": "أَ", "uzbek_translation": "A (fatha)", "transliteration": "a", "category": "harakat"},
    {"level_id": 1, "arabic_word": "إِ", "uzbek_translation": "I (kasra)", "transliteration": "i", "category": "harakat"},
    {"level_id": 1, "arabic_word": "أُ", "uzbek_translation": "U (damma)", "transliteration": "u", "category": "harakat"},
    {"level_id": 1, "arabic_word": "بَ", "uzbek_translation": "Ba (bo'", "transliteration": "ba", "category": "harf"},
    {"level_id": 1, "arabic_word": "تَ", "uzbek_translation": "Ta (to')", "transliteration": "ta", "category": "harf"},
    {"level_id": 1, "arabic_word": "ثَ", "uzbek_translation": "Sa (so')", "transliteration": "sa", "category": "harf"},
    {"level_id": 1, "arabic_word": "نُورٌ", "uzbek_translation": "Nur (yorug'lik)", "transliteration": "nuur", "category": "soʻz"},
    {"level_id": 1, "arabic_word": "بَابٌ", "uzbek_translation": "Eshik", "transliteration": "baab", "category": "soʻz",
     "example_sentence_arabic": "هَذَا بَابٌ", "example_sentence_uzbek": "Bu eshik"},
    {"level_id": 1, "arabic_word": "كِتَابٌ", "uzbek_translation": "Kitob", "transliteration": "kitaab", "category": "soʻz",
     "example_sentence_arabic": "هَذَا كِتَابٌ", "example_sentence_uzbek": "Bu kitob"},
    {"level_id": 1, "arabic_word": "قَلَمٌ", "uzbek_translation": "Qalam", "transliteration": "qalam", "category": "soʻz",
     "example_sentence_arabic": "هَذَا قَلَمٌ", "example_sentence_uzbek": "Bu qalam"},

    # ─── Level 2: Gate of Sounds — Basic Words ───────────────────────────────
    {"level_id": 2, "arabic_word": "بَيْتٌ", "uzbek_translation": "Uy", "transliteration": "bayt", "category": "uy",
     "example_sentence_arabic": "هَذَا بَيْتٌ كَبِيرٌ", "example_sentence_uzbek": "Bu katta uy"},
    {"level_id": 2, "arabic_word": "مَسْجِدٌ", "uzbek_translation": "Masjid", "transliteration": "masjid", "category": "joy"},
    {"level_id": 2, "arabic_word": "مَدْرَسَةٌ", "uzbek_translation": "Maktab", "transliteration": "madrasa", "category": "joy"},
    {"level_id": 2, "arabic_word": "طَالِبٌ", "uzbek_translation": "Talaba", "transliteration": "taalib", "category": "odam"},
    {"level_id": 2, "arabic_word": "مُعَلِّمٌ", "uzbek_translation": "O'qituvchi", "transliteration": "mu'allim", "category": "odam"},
    {"level_id": 2, "arabic_word": "هَذَا", "uzbek_translation": "Bu (erkak)", "transliteration": "haazaa", "category": "ko'rsatish"},
    {"level_id": 2, "arabic_word": "هَذِهِ", "uzbek_translation": "Bu (ayol)", "transliteration": "haazihi", "category": "ko'rsatish"},
    {"level_id": 2, "arabic_word": "ذَلِكَ", "uzbek_translation": "U (erkak)", "transliteration": "zaalika", "category": "ko'rsatish"},
    {"level_id": 2, "arabic_word": "كَبِيرٌ", "uzbek_translation": "Katta", "transliteration": "kabiir", "category": "sifat"},
    {"level_id": 2, "arabic_word": "صَغِيرٌ", "uzbek_translation": "Kichik", "transliteration": "saghiir", "category": "sifat"},

    # ─── Level 3: Valley of Identity — Pronouns & Gender ─────────────────────
    {"level_id": 3, "arabic_word": "أَنَا", "uzbek_translation": "Men", "transliteration": "ana", "category": "zamir"},
    {"level_id": 3, "arabic_word": "أَنْتَ", "uzbek_translation": "Sen (erkak)", "transliteration": "anta", "category": "zamir"},
    {"level_id": 3, "arabic_word": "أَنْتِ", "uzbek_translation": "Sen (ayol)", "transliteration": "anti", "category": "zamir"},
    {"level_id": 3, "arabic_word": "هُوَ", "uzbek_translation": "U (erkak)", "transliteration": "huwa", "category": "zamir"},
    {"level_id": 3, "arabic_word": "هِيَ", "uzbek_translation": "U (ayol)", "transliteration": "hiya", "category": "zamir"},
    {"level_id": 3, "arabic_word": "نَحْنُ", "uzbek_translation": "Biz", "transliteration": "nahnu", "category": "zamir"},
    {"level_id": 3, "arabic_word": "أَنْتُمْ", "uzbek_translation": "Sizlar (erkak)", "transliteration": "antum", "category": "zamir"},
    {"level_id": 3, "arabic_word": "هُمْ", "uzbek_translation": "Ular (erkak)", "transliteration": "hum", "category": "zamir"},
    {"level_id": 3, "arabic_word": "هُنَّ", "uzbek_translation": "Ular (ayol)", "transliteration": "hunna", "category": "zamir"},
    {"level_id": 3, "arabic_word": "مَنْ", "uzbek_translation": "Kim?", "transliteration": "man", "category": "savol"},
    {"level_id": 3, "arabic_word": "مَا", "uzbek_translation": "Nima?", "transliteration": "maa", "category": "savol"},

    # ─── Level 4: Marketplace & Household — Nouns I ──────────────────────────
    {"level_id": 4, "arabic_word": "سُوقٌ", "uzbek_translation": "Bozor", "transliteration": "suuq", "category": "joy"},
    {"level_id": 4, "arabic_word": "خُبْزٌ", "uzbek_translation": "Non", "transliteration": "khubz", "category": "oziq"},
    {"level_id": 4, "arabic_word": "مَاءٌ", "uzbek_translation": "Suv", "transliteration": "maa'", "category": "oziq"},
    {"level_id": 4, "arabic_word": "طَعَامٌ", "uzbek_translation": "Taom", "transliteration": "ta'aam", "category": "oziq"},
    {"level_id": 4, "arabic_word": "شَايٌ", "uzbek_translation": "Choy", "transliteration": "shaay", "category": "oziq"},
    {"level_id": 4, "arabic_word": "تُفَّاحٌ", "uzbek_translation": "Olma", "transliteration": "tuffaah", "category": "oziq"},
    {"level_id": 4, "arabic_word": "سَيَّارَةٌ", "uzbek_translation": "Mashina", "transliteration": "sayyaara", "category": "transport"},
    {"level_id": 4, "arabic_word": "طَرِيقٌ", "uzbek_translation": "Yo'l", "transliteration": "tariiq", "category": "joy"},
    {"level_id": 4, "arabic_word": "مَكْتَبٌ", "uzbek_translation": "Ish stoli / Ofis", "transliteration": "maktab", "category": "uy"},
    {"level_id": 4, "arabic_word": "كُرْسِيٌّ", "uzbek_translation": "Stul", "transliteration": "kursi", "category": "uy"},

    # ─── Level 5: Household — Nouns II ───────────────────────────────────────
    {"level_id": 5, "arabic_word": "غُرْفَةٌ", "uzbek_translation": "Xona", "transliteration": "ghurfa", "category": "uy"},
    {"level_id": 5, "arabic_word": "نَافِذَةٌ", "uzbek_translation": "Deraza", "transliteration": "naafiza", "category": "uy"},
    {"level_id": 5, "arabic_word": "مَطْبَخٌ", "uzbek_translation": "Oshxona", "transliteration": "matbakh", "category": "uy"},
    {"level_id": 5, "arabic_word": "حَمَّامٌ", "uzbek_translation": "Hammom", "transliteration": "hammaam", "category": "uy"},
    {"level_id": 5, "arabic_word": "سَرِيرٌ", "uzbek_translation": "Karavot", "transliteration": "sariir", "category": "uy"},
    {"level_id": 5, "arabic_word": "مِفْتَاحٌ", "uzbek_translation": "Kalit", "transliteration": "miftaah", "category": "buyum"},
    {"level_id": 5, "arabic_word": "هَاتِفٌ", "uzbek_translation": "Telefon", "transliteration": "haatif", "category": "buyum"},
    {"level_id": 5, "arabic_word": "سَاعَةٌ", "uzbek_translation": "Soat", "transliteration": "saa'a", "category": "buyum"},
    {"level_id": 5, "arabic_word": "مَلَابِسٌ", "uzbek_translation": "Kiyimlar", "transliteration": "malaabis", "category": "kiyim"},
    {"level_id": 5, "arabic_word": "حَقِيبَةٌ", "uzbek_translation": "Sumka", "transliteration": "haqiiba", "category": "kiyim"},

    # ─── Level 6: Grove of Actions — Past Tense ──────────────────────────────
    {"level_id": 6, "arabic_word": "كَتَبَ", "uzbek_translation": "Yozdi", "transliteration": "kataba", "category": "fe'l",
     "example_sentence_arabic": "كَتَبَ الطَّالِبُ الدَّرْسَ", "example_sentence_uzbek": "Talaba darsni yozdi"},
    {"level_id": 6, "arabic_word": "قَرَأَ", "uzbek_translation": "O'qidi", "transliteration": "qara'a", "category": "fe'l"},
    {"level_id": 6, "arabic_word": "ذَهَبَ", "uzbek_translation": "Ketdi", "transliteration": "zahaba", "category": "fe'l"},
    {"level_id": 6, "arabic_word": "أَكَلَ", "uzbek_translation": "Yedi", "transliteration": "akala", "category": "fe'l"},
    {"level_id": 6, "arabic_word": "شَرِبَ", "uzbek_translation": "Ichdi", "transliteration": "shariba", "category": "fe'l"},
    {"level_id": 6, "arabic_word": "جَلَسَ", "uzbek_translation": "O'tirdi", "transliteration": "jalasa", "category": "fe'l"},
    {"level_id": 6, "arabic_word": "نَامَ", "uzbek_translation": "Uxladi", "transliteration": "naama", "category": "fe'l"},
    {"level_id": 6, "arabic_word": "فَتَحَ", "uzbek_translation": "Ochdi", "transliteration": "fataha", "category": "fe'l"},
    {"level_id": 6, "arabic_word": "أَخَذَ", "uzbek_translation": "Oldi", "transliteration": "akhaza", "category": "fe'l"},
    {"level_id": 6, "arabic_word": "دَخَلَ", "uzbek_translation": "Kirdi", "transliteration": "dakhala", "category": "fe'l"},

    # ─── Level 7: Grove of Actions — Present Tense ───────────────────────────
    {"level_id": 7, "arabic_word": "يَكْتُبُ", "uzbek_translation": "Yozmoqda", "transliteration": "yaktubu", "category": "fe'l"},
    {"level_id": 7, "arabic_word": "يَقْرَأُ", "uzbek_translation": "O'qimoqda", "transliteration": "yaqra'u", "category": "fe'l"},
    {"level_id": 7, "arabic_word": "يَذْهَبُ", "uzbek_translation": "Ketmoqda", "transliteration": "yazhabu", "category": "fe'l"},
    {"level_id": 7, "arabic_word": "يَأْكُلُ", "uzbek_translation": "Yemoqda", "transliteration": "ya'kulu", "category": "fe'l"},
    {"level_id": 7, "arabic_word": "يَشْرَبُ", "uzbek_translation": "Ichmoqda", "transliteration": "yashrabu", "category": "fe'l"},
    {"level_id": 7, "arabic_word": "يُصَلِّي", "uzbek_translation": "Namoz o'qimoqda", "transliteration": "yusalli", "category": "fe'l"},
    {"level_id": 7, "arabic_word": "يَعْلَمُ", "uzbek_translation": "Bilmoqda", "transliteration": "ya'lamu", "category": "fe'l"},
    {"level_id": 7, "arabic_word": "يَقُولُ", "uzbek_translation": "Aytmoqda", "transliteration": "yaquulu", "category": "fe'l"},
    {"level_id": 7, "arabic_word": "يَسْمَعُ", "uzbek_translation": "Eshitmoqda", "transliteration": "yasma'u", "category": "fe'l"},
    {"level_id": 7, "arabic_word": "يَنْظُرُ", "uzbek_translation": "Qarmoqda", "transliteration": "yanzuru", "category": "fe'l"},

    # ─── Level 8: Sentence Building ───────────────────────────────────────────
    {"level_id": 8, "arabic_word": "فِي", "uzbek_translation": "Ichida / Da", "transliteration": "fii", "category": "bog'lovchi"},
    {"level_id": 8, "arabic_word": "عَلَى", "uzbek_translation": "Ustida", "transliteration": "'alaa", "category": "bog'lovchi"},
    {"level_id": 8, "arabic_word": "مِنْ", "uzbek_translation": "Dan", "transliteration": "min", "category": "bog'lovchi"},
    {"level_id": 8, "arabic_word": "إِلَى", "uzbek_translation": "Ga qarab", "transliteration": "ilaa", "category": "bog'lovchi"},
    {"level_id": 8, "arabic_word": "مَعَ", "uzbek_translation": "Bilan", "transliteration": "ma'a", "category": "bog'lovchi"},
    {"level_id": 8, "arabic_word": "لَا", "uzbek_translation": "Yo'q / Emas", "transliteration": "laa", "category": "inkor"},
    {"level_id": 8, "arabic_word": "نَعَمْ", "uzbek_translation": "Ha", "transliteration": "na'am", "category": "javob"},
    {"level_id": 8, "arabic_word": "جَيِّدٌ", "uzbek_translation": "Yaxshi", "transliteration": "jayyid", "category": "sifat"},
    {"level_id": 8, "arabic_word": "جَمِيلٌ", "uzbek_translation": "Chiroyli", "transliteration": "jamiil", "category": "sifat"},
    {"level_id": 8, "arabic_word": "كَثِيرٌ", "uzbek_translation": "Ko'p", "transliteration": "kasiir", "category": "sifat"},

    # ─── Level 9: Wise Scholar — Complex Vocabulary ───────────────────────────
    {"level_id": 9, "arabic_word": "الْعِلْمُ", "uzbek_translation": "Ilm (bilim)", "transliteration": "al-'ilm", "category": "islom"},
    {"level_id": 9, "arabic_word": "الْإِيمَانُ", "uzbek_translation": "Iymon", "transliteration": "al-iimaan", "category": "islom"},
    {"level_id": 9, "arabic_word": "الصَّلَاةُ", "uzbek_translation": "Namoz", "transliteration": "as-salaah", "category": "islom"},
    {"level_id": 9, "arabic_word": "الصِّيَامُ", "uzbek_translation": "Ro'za", "transliteration": "as-siyaam", "category": "islom"},
    {"level_id": 9, "arabic_word": "الزَّكَاةُ", "uzbek_translation": "Zakot", "transliteration": "az-zakaah", "category": "islom"},
    {"level_id": 9, "arabic_word": "الْحَجُّ", "uzbek_translation": "Haj", "transliteration": "al-hajj", "category": "islom"},
    {"level_id": 9, "arabic_word": "الْقُرْآنُ", "uzbek_translation": "Qur'on", "transliteration": "al-qur'aan", "category": "islom"},
    {"level_id": 9, "arabic_word": "الرَّحْمَةُ", "uzbek_translation": "Rahmat (marhamat)", "transliteration": "ar-rahma", "category": "islom"},
    {"level_id": 9, "arabic_word": "الصَّبْرُ", "uzbek_translation": "Sabr", "transliteration": "as-sabr", "category": "islom"},
    {"level_id": 9, "arabic_word": "الشُّكْرُ", "uzbek_translation": "Shukr", "transliteration": "ash-shukr", "category": "islom"},

    # ─── Level 10: The Wise Scholar — Quranic Phrases ────────────────────────
    {"level_id": 10, "arabic_word": "بِسْمِ اللَّهِ", "uzbek_translation": "Alloh nomi bilan", "transliteration": "bismillah", "category": "dua"},
    {"level_id": 10, "arabic_word": "الْحَمْدُ لِلَّهِ", "uzbek_translation": "Barcha maqtovlar Allohga", "transliteration": "alhamdulillah", "category": "dua"},
    {"level_id": 10, "arabic_word": "سُبْحَانَ اللَّهِ", "uzbek_translation": "Alloh pok", "transliteration": "subhanallah", "category": "dua"},
    {"level_id": 10, "arabic_word": "اللَّهُ أَكْبَرُ", "uzbek_translation": "Alloh buyuk", "transliteration": "allahu akbar", "category": "dua"},
    {"level_id": 10, "arabic_word": "لَا إِلَهَ إِلَّا اللَّهُ", "uzbek_translation": "Allohdan boshqa iloh yo'q", "transliteration": "la ilaha illallah", "category": "dua"},
    {"level_id": 10, "arabic_word": "إِنْ شَاءَ اللَّهُ", "uzbek_translation": "Alloh xohlasa", "transliteration": "inshallah", "category": "dua"},
    {"level_id": 10, "arabic_word": "مَاشَاءَ اللَّهُ", "uzbek_translation": "Alloh nimalikini xohladi", "transliteration": "mashallah", "category": "dua"},
    {"level_id": 10, "arabic_word": "جَزَاكَ اللَّهُ خَيْرًا", "uzbek_translation": "Alloh sizga yaxshilik bersin", "transliteration": "jazakallahu khayran", "category": "dua"},
    {"level_id": 10, "arabic_word": "أَسْتَغْفِرُ اللَّهَ", "uzbek_translation": "Allohdan mag'firat so'rayman", "transliteration": "astaghfirullah", "category": "dua"},
    {"level_id": 10, "arabic_word": "تَوَكَّلْتُ عَلَى اللَّهِ", "uzbek_translation": "Allohga tavakkal qildim", "transliteration": "tawakkaltu 'alallah", "category": "dua"},
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        existing = await session.execute(select(Vocabulary))
        if existing.scalars().first():
            print("Database already has vocabulary. Skipping seed.")
            return

        for item in VOCABULARY:
            word = Vocabulary(**item)
            session.add(word)

        await session.commit()
        print(f"Seeded {len(VOCABULARY)} vocabulary words across 10 levels.")


if __name__ == "__main__":
    asyncio.run(seed())
