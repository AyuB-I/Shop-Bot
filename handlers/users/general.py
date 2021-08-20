from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, _
from states.general import GeneralStates
from states.shoes import ShoesStates
from keyboards.defualt import home_page, shoes


@dp.message_handler(text=_("Главная\U00002B06"), state="*")
async def home(message: types.Message, state: FSMContext):
    await message.answer(text="Чтобы купить обувь выберите \"Обувь\"", reply_markup=home_page)
    await state.reset_state()


@dp.message_handler(text=_("Назад\U00002B05"), state=ShoesStates)
async def back(message: types.Message):
    await message.answer(text=_("Что вы хотите купить?"), reply_markup=shoes)
    await ShoesStates.choosing_type.set()
