from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import ArabicLevel
from bot.database.repository import UserRepository
from bot.keyboards.main_kb import main_menu_kb, arabic_level_kb, back_to_menu_kb
from bot.utils.messages import WELCOME, ASK_NAME, ASK_AGE, ASK_ARABIC_LEVEL, REGISTRATION_DONE, MAIN_MENU

router = Router()


class RegStates(StatesGroup):
    waiting_name = State()
    waiting_age = State()
    waiting_arabic_level = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, user, session: AsyncSession):
    if user.is_registered:
        await state.clear()
        await message.answer(MAIN_MENU, reply_markup=main_menu_kb())
        return

    await message.answer(WELCOME)
    await message.answer(ASK_NAME)
    await state.set_state(RegStates.waiting_name)


@router.message(RegStates.waiting_name)
async def reg_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2 or len(name) > 60:
        await message.answer("Iltimos, to'g'ri ism kiriting (2-60 ta harf).")
        return
    await state.update_data(full_name=name)
    await message.answer(ASK_AGE)
    await state.set_state(RegStates.waiting_age)


@router.message(RegStates.waiting_age)
async def reg_age(message: Message, state: FSMContext):
    try:
        age = int(message.text.strip())
        if age < 5 or age > 100:
            raise ValueError
    except ValueError:
        await message.answer("Iltimos, to'g'ri yosh kiriting (5-100 oralig'ida raqam).")
        return
    await state.update_data(age=age)
    await message.answer(ASK_ARABIC_LEVEL, reply_markup=arabic_level_kb())
    await state.set_state(RegStates.waiting_arabic_level)


@router.callback_query(RegStates.waiting_arabic_level, F.data.startswith("reg_level:"))
async def reg_arabic_level(callback: CallbackQuery, state: FSMContext, user, session: AsyncSession):
    level_str = callback.data.split(":")[1]
    level_map = {
        "beginner": ArabicLevel.BEGINNER,
        "elementary": ArabicLevel.ELEMENTARY,
        "intermediate": ArabicLevel.INTERMEDIATE,
    }
    arabic_level = level_map.get(level_str, ArabicLevel.BEGINNER)

    data = await state.get_data()
    repo = UserRepository(session)
    await repo.update(
        user.user_id,
        full_name=data.get("full_name", ""),
        age=data.get("age"),
        arabic_level=arabic_level,
        is_registered=True,
    )
    await state.clear()

    await callback.message.edit_text(REGISTRATION_DONE)
    await callback.message.answer(MAIN_MENU, reply_markup=main_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "menu:main")
async def menu_main(callback: CallbackQuery, state: FSMContext, user):
    if not user.is_registered:
        await callback.answer("Avval ro'yxatdan o'ting!", show_alert=True)
        return
    await state.clear()
    await callback.message.edit_text(MAIN_MENU, reply_markup=main_menu_kb())
    await callback.answer()


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext, user):
    if not user.is_registered:
        await message.answer("Avval /start orqali ro'yxatdan o'ting.")
        return
    await state.clear()
    await message.answer(MAIN_MENU, reply_markup=main_menu_kb())
