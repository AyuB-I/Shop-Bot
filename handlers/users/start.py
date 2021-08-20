from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from keyboards.defualt import home_page
from keyboards.inline import language
from loader import dp

from states.general import SettingStates

from database import DBCommands

db = DBCommands()


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    user = await db.get_user(message.from_user.id)
    if user:
        return user
    await db.add_user()
    await message.answer(text="Приветствуем вас {full_name}".format(full_name=message.from_user.full_name))
    await message.answer(text="Выберите язык!", reply_markup=language)
    await SettingStates.getting_language.set()


@dp.callback_query_handler(text_contains="uz", state=SettingStates.getting_language)
async def set_language_uz(call: types.CallbackQuery):
    await db.set_language("uz")
    await call.message.edit_reply_markup()
    await call.message.answer("Siz O'bek tilini tanladingiz!", reply_markup=home_page)


@dp.callback_query_handler(text_contains="ru", state=SettingStates.getting_language)
async def set_language_uz(call: types.CallbackQuery):
    await db.set_language("ru")
    await call.message.edit_reply_markup()
    await call.message.answer("Вы выбрали Русский язык!", reply_markup=home_page)
