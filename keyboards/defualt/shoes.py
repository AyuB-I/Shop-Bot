from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


shoes = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_("Кроссовки")),
            KeyboardButton(text=_("Мокасины"))
        ],
        [
            KeyboardButton(text=_("Главная\U00002B06"))
        ]
    ],
    resize_keyboard=True
)
