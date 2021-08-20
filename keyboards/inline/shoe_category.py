from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


shoe_category = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Кроссовка"), callback_data="category_sneakers"),
            InlineKeyboardButton(text=_("Мокасина"), callback_data="category_moccasins")
        ]
    ]
)
