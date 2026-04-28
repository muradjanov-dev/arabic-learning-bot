from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class AdminUserCb(CallbackData, prefix="au"):
    user_id: int
    action: str  # "view" | "ban" | "unban" | "set_free" | "set_premium" | "set_unlimited"


class AdminPageCb(CallbackData, prefix="ap"):
    page: int


class PaymentApprovalCb(CallbackData, prefix="pay"):
    request_id: int
    action: str  # "approve" | "decline"


def admin_main_kb(pending_payments: int = 0) -> InlineKeyboardMarkup:
    pay_label = f"💳 To'lovlar ({pending_payments} kutilmoqda)" if pending_payments else "💳 To'lovlar"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin:stats")],
        [InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin:users:0")],
        [InlineKeyboardButton(text=pay_label, callback_data="admin:payments")],
        [InlineKeyboardButton(text="📢 Broadcast", callback_data="admin:broadcast")],
        [InlineKeyboardButton(text="📖 So'z qo'shish", callback_data="admin:add_word")],
    ])


def admin_stats_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Bugun", callback_data="admin:stats:today"),
            InlineKeyboardButton(text="Hafta", callback_data="admin:stats:week"),
            InlineKeyboardButton(text="Oy", callback_data="admin:stats:month"),
        ],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:main")],
    ])


def admin_users_kb(users, page: int, total: int, per_page: int = 10) -> InlineKeyboardMarkup:
    buttons = []
    for u in users:
        tier_icon = {"free": "🆓", "premium": "💎", "unlimited": "♾️"}.get(u.subscription_tier.value, "🆓")
        label = f"{tier_icon} {u.full_name or 'Nomsiz'} | Lv{u.current_level}"
        buttons.append([InlineKeyboardButton(
            text=label,
            callback_data=AdminUserCb(user_id=u.user_id, action="view").pack()
        )])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=AdminPageCb(page=page - 1).pack()))
    if (page + 1) * per_page < total:
        nav.append(InlineKeyboardButton(text="➡️", callback_data=AdminPageCb(page=page + 1).pack()))
    if nav:
        buttons.append(nav)

    buttons.append([InlineKeyboardButton(text="🔍 Qidirish", callback_data="admin:search")])
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_user_detail_kb(user_id: int, is_banned: bool, tier: str) -> InlineKeyboardMarkup:
    ban_text = "✅ Blokdan chiqarish" if is_banned else "🚫 Bloklash"
    ban_action = "unban" if is_banned else "ban"

    tier_buttons = []
    if tier != "free":
        tier_buttons.append(InlineKeyboardButton(
            text="🆓 Free", callback_data=AdminUserCb(user_id=user_id, action="set_free").pack()
        ))
    if tier != "premium":
        tier_buttons.append(InlineKeyboardButton(
            text="💎 Premium", callback_data=AdminUserCb(user_id=user_id, action="set_premium").pack()
        ))
    if tier != "unlimited":
        tier_buttons.append(InlineKeyboardButton(
            text="♾️ Unlimited", callback_data=AdminUserCb(user_id=user_id, action="set_unlimited").pack()
        ))

    buttons = [
        tier_buttons,
        [InlineKeyboardButton(
            text=ban_text,
            callback_data=AdminUserCb(user_id=user_id, action=ban_action).pack()
        )],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:users:0")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def payment_approval_kb(request_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlash",
                callback_data=PaymentApprovalCb(request_id=request_id, action="approve").pack()
            ),
            InlineKeyboardButton(
                text="❌ Rad etish",
                callback_data=PaymentApprovalCb(request_id=request_id, action="decline").pack()
            ),
        ]
    ])


def admin_broadcast_confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha, yuborish", callback_data="admin:broadcast:confirm"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:main"),
        ]
    ])


def admin_back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Admin panel", callback_data="admin:main")],
    ])
