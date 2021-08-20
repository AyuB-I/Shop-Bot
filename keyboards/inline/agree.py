from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import _

agree = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Согласен"), callback_data="agree"),
            InlineKeyboardButton(text=_("Отменить"), callback_data="cancel")
        ]
    ]
)
