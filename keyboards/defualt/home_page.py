from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


home_page = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_("Обувь\U0001F45F"))
        ],
        [
            KeyboardButton(text=_("Корзина\U0001F6D2")),
            KeyboardButton(text=_("Настройки\U00002699"))
        ]
    ],
    resize_keyboard=True
)
