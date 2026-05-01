import logging
from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.database.models import SubscriptionTier
from bot.database.repository import UserRepository, LessonRepository, VocabularyRepository, PaymentRepository
from bot.keyboards.admin_kb import (
    admin_main_kb, admin_stats_kb, admin_users_kb,
    admin_user_detail_kb, admin_broadcast_confirm_kb, admin_back_kb,
    AdminUserCb, AdminPageCb, PaymentApprovalCb,
)
from bot.utils.messages import (
    ADMIN_MAIN, ADMIN_STATS_HEADER, ADMIN_USER_LIST_HEADER,
    ADMIN_USER_DETAIL, BROADCAST_ASK, BROADCAST_CONFIRM, BROADCAST_DONE,
    PAYMENT_APPROVED, PAYMENT_DECLINED,
    ADMIN_PAYMENT_APPROVED_MARK, ADMIN_PAYMENT_DECLINED_MARK,
)

logger = logging.getLogger(__name__)
router = Router()
PER_PAGE = 10


def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS


class AdminStates(StatesGroup):
    broadcast_message = State()
    broadcast_confirm = State()
    search_user = State()
    add_word_arabic = State()
    add_word_uzbek = State()
    add_word_level = State()
    decline_reason = State()


# ── Gemini content generation ─────────────────────────────────────────────────

@router.message(Command("genwords"))
async def cmd_genwords(message: Message):
    """Admin: /genwords [level] — generate Gemini example sentences for empty vocabulary words."""
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q.")
        return

    from bot.config import settings
    if not settings.GEMINI_API_KEY:
        await message.answer(
            "❌ GEMINI_API_KEY sozlanmagan.\n\n"
            "1. https://aistudio.google.com/apikey dan bepul API key oling\n"
            "2. Railway → Variables → GEMINI_API_KEY qo'shing"
        )
        return

    # Optional level filter: /genwords 5
    parts = message.text.split()
    level_filter = None
    if len(parts) > 1 and parts[1].isdigit():
        level_filter = int(parts[1])

    import asyncio
    from bot.database.base import async_session_maker
    from bot.services.gemini_service import bulk_generate_missing

    label = f"{level_filter}-daraja uchun" if level_filter else "barcha darajalar uchun"
    await message.answer(f"🤖 Gemini content generation boshlandi — {label}.\nAdmin panelga progress keladi.")
    asyncio.create_task(bulk_generate_missing(async_session_maker, message.bot, message.chat.id, level_filter))


# ── Entry ─────────────────────────────────────────────────────────────────────

@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q.")
        return
    await state.clear()
    pay_repo = PaymentRepository(session)
    pending = await pay_repo.count_pending()
    await message.answer(ADMIN_MAIN, reply_markup=admin_main_kb(pending))


@router.callback_query(F.data == "admin:main")
async def admin_main(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return
    await state.clear()
    pay_repo = PaymentRepository(session)
    pending = await pay_repo.count_pending()
    await callback.message.edit_text(ADMIN_MAIN, reply_markup=admin_main_kb(pending))
    await callback.answer()


# ── Reset commands ───────────────────────────────────────────────────────────

@router.message(Command("resetme"))
async def cmd_resetme(message: Message, session: AsyncSession):
    """Admin only: wipe your own progress and re-register from scratch."""
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q.")
        return
    from sqlalchemy import delete
    from bot.database.models import UserProgress, Lesson as LessonModel, SubscriptionTier
    uid = message.from_user.id
    await session.execute(delete(UserProgress).where(UserProgress.user_id == uid))
    await session.execute(delete(LessonModel).where(LessonModel.user_id == uid))
    repo = UserRepository(session)
    await repo.update(
        uid,
        is_registered=False,
        current_level=1,
        current_topic=1,
        current_xp=0,
        streak_days=0,
        achievements_earned="",
        shijoat_pin_id=None,
        daily_lessons_done=0,
        referred_by=None,
        last_active_date=None,
        subscription_tier=SubscriptionTier.FREE,
        subscription_expires=None,
        shijoat_points=100,
        trial_given=False,
    )
    await session.commit()
    await message.answer("✅ Ma'lumotlaringiz tozalandi. /start bilan qayta boshlang.")


@router.message(Command("resetall"))
async def cmd_resetall(message: Message, session: AsyncSession):
    """Admin only: wipe ALL users' progress (keeps accounts, re-registration required)."""
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q.")
        return
    from sqlalchemy import delete, update
    from bot.database.models import UserProgress, Lesson as LessonModel, User, SubscriptionTier
    await session.execute(delete(UserProgress))
    await session.execute(delete(LessonModel))
    await session.execute(
        update(User).values(
            is_registered=False,
            current_level=1,
            current_topic=1,
            current_xp=0,
            streak_days=0,
            achievements_earned="",
            shijoat_pin_id=None,
            daily_lessons_done=0,
            referred_by=None,
            last_active_date=None,
            subscription_tier=SubscriptionTier.FREE,
            subscription_expires=None,
            shijoat_points=100,
            trial_given=False,
        )
    )
    await session.commit()
    await message.answer(f"✅ Barcha foydalanuvchilar qayta boshlash uchun tozalandi.")


# ── Statistics ────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:stats")
async def admin_stats(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    user_repo = UserRepository(session)
    total = await user_repo.count_total()
    premium = await user_repo.count_by_tier(SubscriptionTier.PREMIUM)
    unlimited = await user_repo.count_by_tier(SubscriptionTier.UNLIMITED)

    text = (
        f"{ADMIN_STATS_HEADER}"
        f"👥 Jami foydalanuvchilar: <b>{total}</b>\n"
        f"💎 Premium: <b>{premium}</b>\n"
        f"♾️ Cheksiz: <b>{unlimited}</b>\n\n"
        f"Quyidagi davr bo'yicha ko'rish uchun tanlang:"
    )
    await callback.message.edit_text(text, reply_markup=admin_stats_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("admin:stats:"))
async def admin_stats_period(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    period = callback.data.split(":")[-1]
    now = datetime.utcnow()
    if period == "today":
        since = now.replace(hour=0, minute=0, second=0, microsecond=0)
        period_label = "Bugun"
    elif period == "week":
        since = now - timedelta(days=7)
        period_label = "Oxirgi 7 kun"
    else:
        since = now - timedelta(days=30)
        period_label = "Oxirgi 30 kun"

    user_repo = UserRepository(session)
    lesson_repo = LessonRepository(session)

    new_users = await user_repo.count_new_since(since)
    active_users = await user_repo.count_active_since(since)
    lessons = await lesson_repo.count_completed_since(since)
    total = await user_repo.count_total()

    text = (
        f"{ADMIN_STATS_HEADER}"
        f"📅 Davr: <b>{period_label}</b>\n\n"
        f"👤 Yangi foydalanuvchilar: <b>{new_users}</b>\n"
        f"⚡ Faol foydalanuvchilar: <b>{active_users}</b>\n"
        f"📖 Yakunlangan darslar: <b>{lessons}</b>\n"
        f"👥 Jami foydalanuvchilar: <b>{total}</b>"
    )
    await callback.message.edit_text(text, reply_markup=admin_stats_kb())
    await callback.answer()


# ── User list ─────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("admin:users:"))
async def admin_users(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    page = int(callback.data.split(":")[-1])
    user_repo = UserRepository(session)
    total = await user_repo.count_total()
    users = await user_repo.list_users(offset=page * PER_PAGE, limit=PER_PAGE)
    total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)

    text = ADMIN_USER_LIST_HEADER.format(total=total)
    text += f"Sahifa {page + 1}/{total_pages}"
    await callback.message.edit_text(text, reply_markup=admin_users_kb(users, page, total, PER_PAGE))
    await callback.answer()


@router.callback_query(AdminPageCb.filter())
async def admin_users_page(callback: CallbackQuery, callback_data: AdminPageCb, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    page = callback_data.page
    user_repo = UserRepository(session)
    total = await user_repo.count_total()
    users = await user_repo.list_users(offset=page * PER_PAGE, limit=PER_PAGE)
    total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)

    text = ADMIN_USER_LIST_HEADER.format(total=total)
    text += f"Sahifa {page + 1}/{total_pages}"
    await callback.message.edit_text(text, reply_markup=admin_users_kb(users, page, total, PER_PAGE))
    await callback.answer()


# ── User detail & actions ─────────────────────────────────────────────────────

@router.callback_query(AdminUserCb.filter(F.action == "view"))
async def admin_user_view(callback: CallbackQuery, callback_data: AdminUserCb, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    repo = UserRepository(session)
    u = await repo.get(callback_data.user_id)
    if not u:
        await callback.answer("Foydalanuvchi topilmadi.", show_alert=True)
        return

    last_active = u.last_active_date.strftime("%d.%m.%Y %H:%M") if u.last_active_date else "Hech qachon"
    join_date = u.join_date.strftime("%d.%m.%Y") if u.join_date else "—"
    arabic_map = {"beginner": "Yangi boshlovchi", "elementary": "O'rta", "intermediate": "Ilg'or"}

    text = ADMIN_USER_DETAIL.format(
        user_id=u.user_id,
        name=u.full_name or "Noma'lum",
        username=u.username or "yo'q",
        age=u.age or "—",
        arabic_level=arabic_map.get(u.arabic_level.value, "—"),
        level=u.current_level,
        xp=u.current_xp,
        streak=u.streak_days,
        shijoat=u.shijoat_points,
        tier=u.subscription_tier.value,
        join_date=join_date,
        last_active=last_active,
        is_banned="Ha 🚫" if u.is_banned else "Yo'q ✅",
    )
    await callback.message.edit_text(
        text,
        reply_markup=admin_user_detail_kb(u.user_id, u.is_banned, u.subscription_tier.value),
    )
    await callback.answer()


@router.callback_query(AdminUserCb.filter(F.action.in_({"ban", "unban"})))
async def admin_user_ban(callback: CallbackQuery, callback_data: AdminUserCb, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    repo = UserRepository(session)
    is_ban = callback_data.action == "ban"
    await repo.update(callback_data.user_id, is_banned=is_ban)
    action_label = "Bloklandi 🚫" if is_ban else "Blok olib tashlandi ✅"
    await callback.answer(action_label)

    u = await repo.get(callback_data.user_id)
    await callback.message.edit_reply_markup(
        reply_markup=admin_user_detail_kb(u.user_id, u.is_banned, u.subscription_tier.value)
    )


@router.callback_query(AdminUserCb.filter(F.action.in_({"set_free", "set_premium", "set_unlimited"})))
async def admin_user_set_tier(callback: CallbackQuery, callback_data: AdminUserCb, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    tier_map = {
        "set_free": SubscriptionTier.FREE,
        "set_premium": SubscriptionTier.PREMIUM,
        "set_unlimited": SubscriptionTier.UNLIMITED,
    }
    new_tier = tier_map[callback_data.action]
    repo = UserRepository(session)

    updates = {"subscription_tier": new_tier}
    if new_tier != SubscriptionTier.FREE:
        updates["subscription_expires"] = datetime.utcnow() + timedelta(days=settings.SUBSCRIPTION_DAYS)
    else:
        updates["subscription_expires"] = None

    await repo.update(callback_data.user_id, **updates)
    await callback.answer(f"Obuna o'zgartirildi: {new_tier.value}")

    u = await repo.get(callback_data.user_id)
    await callback.message.edit_reply_markup(
        reply_markup=admin_user_detail_kb(u.user_id, u.is_banned, u.subscription_tier.value)
    )


# ── Payment approvals ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:payments")
async def admin_payments_list(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    pay_repo = PaymentRepository(session)
    pending = await pay_repo.list_pending(limit=20)
    count = await pay_repo.count_pending()

    if not pending:
        await callback.message.edit_text(
            "Kutilayotgan to'lovlar yo'q. ✅",
            reply_markup=admin_back_kb(),
        )
        await callback.answer()
        return

    from bot.keyboards.admin_kb import admin_back_kb as abk
    await callback.message.edit_text(
        f"<b>Kutilayotgan to'lovlar: {count} ta</b>\n\n"
        "To'lovlar foto sifatida adminlarga yuboriladi. "
        "Tasdiqlash/rad etish tugmalarini bosing.",
        reply_markup=abk(),
    )
    await callback.answer()


@router.callback_query(PaymentApprovalCb.filter(F.action == "approve"))
async def payment_approve(callback: CallbackQuery, callback_data: PaymentApprovalCb, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    pay_repo = PaymentRepository(session)
    req = await pay_repo.get(callback_data.request_id)
    if not req:
        await callback.answer("So'rov topilmadi.", show_alert=True)
        return
    if req.status.value != "pending":
        await callback.answer("Bu so'rov allaqachon ko'rib chiqilgan.", show_alert=True)
        return

    # Activate subscription
    user_repo = UserRepository(session)
    expires = datetime.utcnow() + timedelta(days=settings.SUBSCRIPTION_DAYS)
    shijoat = (
        settings.UNLIMITED_SHIJOAT
        if req.tier == SubscriptionTier.UNLIMITED
        else settings.PREMIUM_DAILY_SHIJOAT
    )
    await user_repo.update(
        req.user_id,
        subscription_tier=req.tier,
        subscription_expires=expires,
        shijoat_points=shijoat,
    )
    await pay_repo.approve(req.id)

    # Notify user
    tier_name = "💎 Premium" if req.tier == SubscriptionTier.PREMIUM else "♾️ Cheksiz"
    user = await user_repo.get(req.user_id)
    from bot.keyboards.main_kb import main_menu_kb
    try:
        await callback.bot.send_message(
            req.user_id,
            PAYMENT_APPROVED.format(
                tier_name=tier_name,
                expires=expires.strftime("%d.%m.%Y"),
                shijoat=shijoat,
            ),
            reply_markup=main_menu_kb(),
        )
    except Exception as e:
        logger.warning(f"Could not notify user {req.user_id}: {e}")

    # Update admin message
    name = user.full_name if user else str(req.user_id)
    await callback.message.edit_caption(
        caption=(callback.message.caption or "") + f"\n\n{ADMIN_PAYMENT_APPROVED_MARK.format(name=name, user_id=req.user_id)}",
        reply_markup=None,
    )
    await callback.answer("Tasdiqlandi ✅")


@router.callback_query(PaymentApprovalCb.filter(F.action == "decline"))
async def payment_decline_prompt(callback: CallbackQuery, callback_data: PaymentApprovalCb, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    await state.set_state(AdminStates.decline_reason)
    await state.update_data(request_id=callback_data.request_id)
    await callback.answer()
    await callback.message.answer(
        "Rad etish sababini kiriting (yoki '-' bosing sabab yo'q bo'lsa):"
    )


@router.message(AdminStates.decline_reason)
async def payment_decline_with_reason(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    request_id = data.get("request_id")
    reason = message.text.strip() if message.text.strip() != "-" else ""
    await state.clear()

    pay_repo = PaymentRepository(session)
    req = await pay_repo.get(request_id)
    if not req:
        await message.answer("So'rov topilmadi.")
        return

    await pay_repo.decline(req.id, reason)

    # Notify user
    reason_text = f"\n\nSabab: {reason}" if reason else ""
    try:
        await message.bot.send_message(
            req.user_id,
            PAYMENT_DECLINED.format(reason=reason_text),
        )
    except Exception as e:
        logger.warning(f"Could not notify user {req.user_id}: {e}")

    user_repo = UserRepository(session)
    user = await user_repo.get(req.user_id)
    name = user.full_name if user else str(req.user_id)
    await message.answer(
        ADMIN_PAYMENT_DECLINED_MARK.format(name=name, user_id=req.user_id),
        reply_markup=admin_back_kb(),
    )


# ── Search ────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:search")
async def admin_search_prompt(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return
    await state.set_state(AdminStates.search_user)
    await callback.message.edit_text("Foydalanuvchi ismini yoki username kiriting:", reply_markup=admin_back_kb())
    await callback.answer()


@router.message(AdminStates.search_user)
async def admin_search_result(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return
    repo = UserRepository(session)
    users = await repo.search_users(message.text.strip())
    await state.clear()

    if not users:
        await message.answer("Foydalanuvchi topilmadi.", reply_markup=admin_back_kb())
        return

    total = len(users)
    text = ADMIN_USER_LIST_HEADER.format(total=total)
    await message.answer(text, reply_markup=admin_users_kb(users, 0, total, PER_PAGE))


# ── Broadcast ─────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:broadcast")
async def admin_broadcast_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return
    await state.set_state(AdminStates.broadcast_message)
    await callback.message.edit_text(BROADCAST_ASK, reply_markup=admin_back_kb())
    await callback.answer()


@router.message(AdminStates.broadcast_message)
async def admin_broadcast_got_message(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return
    repo = UserRepository(session)
    users = await repo.get_all_registered()
    count = len(users)
    await state.update_data(broadcast_text=message.text, broadcast_count=count)
    await state.set_state(AdminStates.broadcast_confirm)
    await message.answer(BROADCAST_CONFIRM.format(count=count), reply_markup=admin_broadcast_confirm_kb())


@router.callback_query(F.data == "admin:broadcast:confirm", AdminStates.broadcast_confirm)
async def admin_broadcast_send(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    data = await state.get_data()
    text = data.get("broadcast_text", "")
    await state.clear()

    repo = UserRepository(session)
    users = await repo.get_all_registered()
    total = len(users)
    sent = 0

    await callback.message.edit_text("Xabar yuborilmoqda...", reply_markup=None)
    await callback.answer()

    for u in users:
        try:
            await callback.bot.send_message(u.user_id, text)
            sent += 1
        except Exception:
            pass

    pay_repo = PaymentRepository(session)
    pending = await pay_repo.count_pending()
    await callback.message.answer(
        BROADCAST_DONE.format(sent=sent, total=total),
        reply_markup=admin_main_kb(pending),
    )


# ── Add vocabulary ────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:add_word")
async def admin_add_word_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return
    await state.set_state(AdminStates.add_word_arabic)
    await callback.message.edit_text("Arabcha so'zni kiriting:", reply_markup=admin_back_kb())
    await callback.answer()


@router.message(AdminStates.add_word_arabic)
async def admin_word_arabic(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.update_data(arabic_word=message.text.strip())
    await message.answer("O'zbekcha tarjimasini kiriting:")
    await state.set_state(AdminStates.add_word_uzbek)


@router.message(AdminStates.add_word_uzbek)
async def admin_word_uzbek(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.update_data(uzbek_translation=message.text.strip())
    await message.answer("Daraja raqamini kiriting (1-10):")
    await state.set_state(AdminStates.add_word_level)


@router.message(AdminStates.add_word_level)
async def admin_word_level(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return
    try:
        level = int(message.text.strip())
        if level < 1 or level > 10:
            raise ValueError
    except ValueError:
        await message.answer("1 dan 10 gacha raqam kiriting.")
        return

    data = await state.get_data()
    await state.clear()

    vocab_repo = VocabularyRepository(session)
    word = await vocab_repo.add_word(
        arabic_word=data["arabic_word"],
        uzbek_translation=data["uzbek_translation"],
        level_id=level,
    )
    pay_repo = PaymentRepository(session)
    pending = await pay_repo.count_pending()
    await message.answer(
        f"So'z qo'shildi!\n\n"
        f"ID: {word.word_id}\n"
        f"Arabcha: {word.arabic_word}\n"
        f"O'zbekcha: {word.uzbek_translation}\n"
        f"Daraja: {word.level_id}",
        reply_markup=admin_main_kb(pending),
    )
