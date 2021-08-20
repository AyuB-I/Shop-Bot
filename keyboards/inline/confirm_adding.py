from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import _

confirm_adding = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Да"), callback_data="yes")
        ],
        [
            InlineKeyboardButton(text=_("Ввести цену заново."), callback_data="change")
        ]
    ]
)
