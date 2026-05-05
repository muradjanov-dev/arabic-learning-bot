import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.database.models import SubscriptionTier
from bot.database.repository import PaymentRepository
from bot.keyboards.main_kb import (
    subscription_kb, back_to_menu_kb, payment_send_receipt_kb, main_menu_kb
)
from bot.keyboards.admin_kb import payment_approval_kb
from bot.utils.messages import (
    SUBSCRIPTION_INFO, PAYMENT_INSTRUCTIONS, PAYMENT_RECEIPT_PROMPT,
    PAYMENT_SENT, ADMIN_PAYMENT_NOTIFICATION,
)

logger = logging.getLogger(__name__)
router = Router()

TIER_META = {
    "premium": {
        "enum": SubscriptionTier.PREMIUM,
        "name": "💎 Premium",
        "price": settings.PREMIUM_PRICE_SOM,
        "display": settings.PREMIUM_PRICE_DISPLAY,
        "shijoat": settings.PREMIUM_DAILY_SHIJOAT,
    },
    "unlimited": {
        "enum": SubscriptionTier.UNLIMITED,
        "name": "♾️ Cheksiz",
        "price": settings.UNLIMITED_PRICE_SOM,
        "display": settings.UNLIMITED_PRICE_DISPLAY,
        "shijoat": settings.UNLIMITED_SHIJOAT,
    },
}


class PaymentStates(StatesGroup):
    waiting_receipt = State()


@router.callback_query(F.data == "menu:subscription")
async def subscription_view(callback: CallbackQuery, user):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return
    text = SUBSCRIPTION_INFO.format(
        premium_price=settings.PREMIUM_PRICE_DISPLAY,
        unlimited_price=settings.UNLIMITED_PRICE_DISPLAY,
    )
    await callback.message.edit_text(text, reply_markup=subscription_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("sub:select:"))
async def subscription_select(callback: CallbackQuery):
    tier_key = callback.data.split(":")[-1]
    meta = TIER_META.get(tier_key)
    if not meta:
        await callback.answer()
        return

    text = PAYMENT_INSTRUCTIONS.format(
        tier_name=meta["name"],
        price=meta["display"],
        card=settings.PAYMENT_CARD_NUMBER,
        holder=settings.PAYMENT_CARD_HOLDER,
        shijoat=meta["shijoat"],
        lessons=meta["shijoat"] // 10,
    )
    await callback.message.edit_text(text, reply_markup=payment_send_receipt_kb(tier_key))
    await callback.answer()


@router.callback_query(F.data.startswith("sub:send_receipt:"))
async def ask_for_receipt(callback: CallbackQuery, state: FSMContext):
    tier_key = callback.data.split(":")[-1]
    meta = TIER_META.get(tier_key)
    if not meta:
        await callback.answer()
        return

    await state.set_state(PaymentStates.waiting_receipt)
    await state.update_data(tier_key=tier_key)
    await callback.message.edit_text(PAYMENT_RECEIPT_PROMPT)
    await callback.answer()


@router.message(PaymentStates.waiting_receipt, F.photo)
async def receive_payment_receipt(message: Message, state: FSMContext, session: AsyncSession, user):
    data = await state.get_data()
    tier_key = data.get("tier_key", "premium")
    meta = TIER_META.get(tier_key, TIER_META["premium"])
    await state.clear()

    photo_file_id = message.photo[-1].file_id

    pay_repo = PaymentRepository(session)
    req = await pay_repo.create(
        user_id=user.user_id,
        tier=meta["enum"],
        amount=meta["price"],
        photo_file_id=photo_file_id,
    )
    await session.commit()

    # Notify user
    await message.answer(PAYMENT_SENT, reply_markup=main_menu_kb())

    # Forward to each admin with approve/decline buttons
    username = user.username or "yo'q"
    caption = ADMIN_PAYMENT_NOTIFICATION.format(
        request_id=req.id,
        name=user.full_name or "Noma'lum",
        user_id=user.user_id,
        username=username,
        tier=meta["name"],
        amount=meta["price"],
        date=datetime.utcnow().strftime("%d.%m.%Y %H:%M"),
    )

    from aiogram import Bot
    bot: Bot = message.bot
    for admin_id in settings.ADMIN_IDS:
        try:
            sent = await bot.send_photo(
                chat_id=admin_id,
                photo=photo_file_id,
                caption=caption,
                reply_markup=payment_approval_kb(req.id),
            )
            await pay_repo.set_admin_message_id(req.id, sent.message_id)
        except Exception as e:
            logger.warning(f"Failed to notify admin {admin_id}: {e}")

    await session.commit()


@router.message(PaymentStates.waiting_receipt)
async def receipt_not_photo(message: Message):
    await message.answer("Iltimos, to'lov chekini rasm (photo) sifatida yuboring.")
