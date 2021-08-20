from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


language = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Uzbekcha", callback_data="uz")
        ],
        [
            InlineKeyboardButton(text="Русский", callback_data="ru")
        ]

    ]
)
