import random
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class AnswerCb(CallbackData, prefix="ans"):
    index: int


class JumbledWordCb(CallbackData, prefix="jw"):
    word_index: int


class JumbledActionCb(CallbackData, prefix="ja"):
    action: str  # "submit" | "reset"


def choice_question_kb(options: List[str], correct_index: int) -> InlineKeyboardMarkup:
    """3-option inline keyboard for visual/audio match questions."""
    buttons = []
    for i, opt in enumerate(options):
        buttons.append([InlineKeyboardButton(text=opt, callback_data=AnswerCb(index=i).pack())])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def jumbled_kb(words: List[str], selected: List[int]) -> InlineKeyboardMarkup:
    """Keyboard for jumbled sentence — shows remaining words + submit/reset."""
    buttons = []
    row = []
    for i, word in enumerate(words):
        if i not in selected:
            row.append(InlineKeyboardButton(text=word, callback_data=JumbledWordCb(word_index=i).pack()))
            if len(row) == 3:
                buttons.append(row)
                row = []
    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(text="🔄 Tozalash", callback_data=JumbledActionCb(action="reset").pack()),
        InlineKeyboardButton(text="✅ Yuborish", callback_data=JumbledActionCb(action="submit").pack()),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def next_question_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Keyingi savol", callback_data="lesson:next")],
    ])


def lesson_result_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Yangi dars", callback_data="menu:lesson")],
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="menu:main")],
    ])
