from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
)

# ── Reply keyboard button labels (must match handler F.text filters) ──────────
KB_LESSON = "📖 Dars boshlash"
KB_PROFILE = "📊 Sahifam"
KB_ROADMAP = "🗺 Yo'lxarita"
KB_LEADERBOARD = "🏆 Reyting"
KB_PREMIUM = "💎 Premium"
KB_SETTINGS = "⚙️ Sozlamalar"


def reply_main_kb() -> ReplyKeyboardMarkup:
    """Persistent keyboard shown at bottom of every chat screen."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=KB_LESSON)],
            [KeyboardButton(text=KB_PROFILE), KeyboardButton(text=KB_ROADMAP)],
            [KeyboardButton(text=KB_LEADERBOARD), KeyboardButton(text=KB_PREMIUM)],
            [KeyboardButton(text=KB_SETTINGS)],
        ],
        resize_keyboard=True,
        persistent=True,
        input_field_placeholder="Quyidagi tugmalardan birini bosing...",
    )


# ── Inline keyboards ──────────────────────────────────────────────────────────

def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Dars boshlash", callback_data="menu:lesson")],
        [
            InlineKeyboardButton(text="📊 Sahifam", callback_data="menu:profile"),
            InlineKeyboardButton(text="🏆 Reyting", callback_data="menu:leaderboard"),
        ],
        [
            InlineKeyboardButton(text="🗺 Yo'lxarita", callback_data="menu:roadmap"),
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="menu:settings"),
        ],
        [InlineKeyboardButton(text="💎 Premium", callback_data="menu:subscription")],
    ])


def arabic_level_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆕 Yangi boshlovchi", callback_data="reg_level:beginner")],
        [InlineKeyboardButton(text="📚 O'rta daraja", callback_data="reg_level:elementary")],
        [InlineKeyboardButton(text="🎓 Ilg'or", callback_data="reg_level:intermediate")],
    ])


def back_to_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")],
    ])


def confirm_lesson_kb(_shijoat: int = 0) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Boshlash!", callback_data="lesson:start")],
        [InlineKeyboardButton(text="🗺 Yo'lxarita", callback_data="menu:roadmap")],
        [InlineKeyboardButton(text="⬅️ Bekor qilish", callback_data="menu:main")],
    ])


def settings_kb(notifications_on: bool) -> InlineKeyboardMarkup:
    notif_text = "🔔 Bildirishnomalar: Yoqilgan ✅" if notifications_on else "🔕 Bildirishnomalar: O'chirilgan ❌"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=notif_text, callback_data="settings:toggle_notif")],
        [InlineKeyboardButton(text="🧠 Qanday ishlaydi?", callback_data="settings:how_it_works")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")],
    ])


def subscription_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Premium — 22,000 so'm (2 hafta)", callback_data="sub:select:premium")],
        [InlineKeyboardButton(text="♾️ Cheksiz — 49,000 so'm (2 hafta)", callback_data="sub:select:unlimited")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")],
    ])


def payment_send_receipt_kb(tier: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Chekni yuborish", callback_data=f"sub:send_receipt:{tier}")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:subscription")],
    ])


def upsell_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Premium xarid qilish", callback_data="sub:select:premium")],
        [InlineKeyboardButton(text="♾️ Cheksiz xarid qilish", callback_data="sub:select:unlimited")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")],
    ])


def renew_subscription_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Obunani yangilash", callback_data="menu:subscription")],
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="menu:main")],
    ])


def roadmap_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Dars boshlash", callback_data="menu:lesson")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")],
    ])
