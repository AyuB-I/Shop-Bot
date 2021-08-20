from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.defualt import home_page
from keyboards.inline import confirm_adding, shoe_category
from loader import dp, _, bot
from database import User, Item
from config import ADMIN_ID
from states.admin_panel import NewItemStates, MailingStates


@dp.message_handler(commands=["cancel"], user_id=ADMIN_ID, state=NewItemStates)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer(_("Вы отменили создание товара."), reply_markup=home_page)
    await state.finish()


@dp.message_handler(user_id=ADMIN_ID, commands="add_item", state="*")
async def add_item(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer(_("Введите название товара."), reply_markup=ReplyKeyboardRemove())
    await NewItemStates.name.set()


@dp.message_handler(user_id=ADMIN_ID, state=NewItemStates.name)
async def add_name(message: types.Message, state: FSMContext):
    item = Item()
    item.name = f"{message.text}"
    await state.update_data(item=item)
    await message.answer(_("Название: <b>{name}</b>\nВыберите категорию товара.").format(name=message.text),
                         reply_markup=shoe_category)
    await NewItemStates.category.set()


@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="category", state=NewItemStates.category)
async def add_category(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    category = call.data[9:]
    data = await state.get_data()
    item: Item = data.get("item")
    item.category = category
    await call.message.answer(_("Название: <b>{name}</b> \nКатегория: {category} \nОтправте фотографию товара.").format(
        name=item.name, category=category))
    await state.update_data(item=item)
    await NewItemStates.photo.set()


@dp.message_handler(user_id=ADMIN_ID, state=NewItemStates.photo, content_types=types.ContentTypes.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    item: Item = data.get("item")
    item.photo = photo
    await message.answer_photo(photo=photo, caption=_("Название: <b>{name}</b>\nКатегория: {category} "
                                                      "\nВведите цену товара в сумах.").format(
        name=item.name, category=item.category))
    await state.update_data(item=item)
    await NewItemStates.price.set()


@dp.message_handler(user_id=ADMIN_ID, state=NewItemStates.price)
async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")
    try:
        price = int(message.text)
    except ValueError:
        await message.answer(_("Неверное значение! Введите число!"))
        return
    item.price = price
    await message.answer_photo(photo=item.photo, caption=_("Название: <b>{name}</b> \nКатегория: {category}\n"
                                                           "Цена: {price}").format(
        name=item.name, category=item.category, price=item.price))
    await message.answer(_("Подтверждаете ли добавление этого товара? Нажмите /cancel чтобы отменить"),
                         reply_markup=confirm_adding)
    await state.update_data(item=item)
    await NewItemStates.confirm.set()


@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="change", state=NewItemStates.confirm)
async def change_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(_("Введите цену товара в сумах."))
    await NewItemStates.price.set()


@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="yes", state=NewItemStates.confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Да", callback_data="yes"),
                types.InlineKeyboardButton(text="Нет", callback_data="no")
            ]
        ]
    )
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get("item")
    await item.create()
    await call.message.answer(_("Товар успешно добавлено!\nРассылять всем?"), reply_markup=markup)
    await MailingStates.mailing.set()


@dp.callback_query_handler(user_id=ADMIN_ID, state=MailingStates, text_contains="no")
async def mailing_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer(text="Рассылка не был создан.", reply_markup=home_page)
    await state.finish()


@dp.callback_query_handler(user_id=ADMIN_ID, state=MailingStates.mailing, text_contains="yes")
async def mailing_confirm(call: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Да", callback_data="yes"),
                types.InlineKeyboardButton(text="Нет", callback_data="no")
            ]
        ]
    )
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get("item")
    await call.message.answer_photo(photo=item.photo, caption=_("<b>{name}</b>\n\n{price} сум").format(name=item.name,
                                                                                                       price=item.price))
    await call.message.answer(_("Подтверждаете ли вы эту рассылку?"), reply_markup=markup)
    await MailingStates.mailing_confirm.set()


@dp.callback_query_handler(user_id=ADMIN_ID, state=MailingStates.mailing_confirm)
async def mailing(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get("item")
    text = ("<b>{name}</b>\n\n{price} сум".format(name=item.name, price=item.price))
    users_ru = await User.query.where(User.language == "ru").gino.all()
    users_uz = await User.query.where(User.language == "uz").gino.all()
    for user_ru in users_ru:
        try:
            await bot.send_message(chat_id=user_ru.user_id, text="\U0001F514 <b>Новый товар!</b>")
            await bot.send_photo(chat_id=user_ru.user_id, photo=item.photo, caption=text)
            await sleep(0.3)
        except Exception:
            await call.message.answer(text=_("Не удалось выполнить рассылку по Русской аудитории!"))
    for user_uz in users_uz:
        try:
            await bot.send_message(chat_id=user_uz.user_id, text="\U0001F514 <b>Yangi tovar!</b>")
            await bot.send_photo(chat_id=user_uz.user_id, photo=item.photo, caption=text)
            await sleep(0.3)
        except Exception:
            await call.message.answer(text=_("Не удалось выполнить рассылку!"))
            await state.finish()
    await call.message.answer(_("Рассылка удачно выполнена!"), reply_markup=home_page)
    await state.finish()
