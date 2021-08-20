from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


basic_controller = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_("Назад\U00002B05")),
            KeyboardButton(text=_("Главная\U00002B06"))
        ]
    ],
    resize_keyboard=True
)