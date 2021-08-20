from asyncio import sleep
from datetime import datetime
from config import ADMIN_ID

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

import database
from loader import dp, _
from keyboards.defualt import shoes, basic_controller
from keyboards.inline import agree
from states.shoes import ShoesStates
from database import DBCommands

db = DBCommands()

buy_item = CallbackData("buy", "item_id")
deleting_item = CallbackData("delete", "item_id")


@dp.message_handler(text=_("Обувь\U0001F45F"), state="*")
async def shop(message: types.Message):
    await message.answer(text=_("Что вы хотите купить?"), reply_markup=shoes)
    await ShoesStates.choosing_type.set()


@dp.message_handler(text=_("Кроссовки"), state=ShoesStates.choosing_type)
async def sneakers(message: types.Message):
    await message.answer(text=_("Вот все кроссовки."), reply_markup=basic_controller)
    items = await db.show_items("sneakers")
    for item in items:
        markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text=_("В корзину"), callback_data=buy_item.new(item_id=item.id))
                ]
            ]
        )
        admin_markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text=_("В корзину"), callback_data=buy_item.new(item_id=item.id)),
                    types.InlineKeyboardButton(text=_("Удалить"), callback_data=deleting_item.new(item_id=item.id))
                ]
            ]
        )
        await message.answer_photo(photo=item.photo, caption=f"<b>{item.name}</b>\n\n{item.price} сум",
                                   reply_markup=admin_markup if message.from_user.id == ADMIN_ID else markup)
        await sleep(0.3)
    await ShoesStates.choosing_shoes.set()


@dp.message_handler(text=_("Мокасины"), state=ShoesStates.choosing_type)
async def sneakers(message: types.Message):
    await message.answer(text=_("Вот все мокасины."), reply_markup=basic_controller)
    items = await db.show_items("moccasins")
    for item in items:
        markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text=_("В корзину"), callback_data=buy_item.new(item_id=item.id))
                ]
            ]
        )
        admin_markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text=_("В корзину"), callback_data=buy_item.new(item_id=item.id)),
                    types.InlineKeyboardButton(text=_("Удалить"), callback_data=deleting_item.new(item_id=item.id))
                ]
            ]
        )
        await message.answer_photo(photo=item.photo, caption=f"<b>{item.name}</b>\n\n{item.price} сум",
                                   reply_markup=admin_markup if message.from_user.id == ADMIN_ID else markup)
        await sleep(0.3)
    await ShoesStates.choosing_shoes.set()


@dp.callback_query_handler(buy_item.filter(), state=ShoesStates.choosing_shoes)
async def buying_item(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = int(callback_data.get("item_id"))
    await call.message.edit_reply_markup()
    item = await database.Item.get(item_id)
    if not item:
        await call.message.answer(text=_("Такого товара не существует."))
        return
    await call.message.answer(text=_("Введите количество!"))
    await ShoesStates.choosing_quantity.set()
    await state.update_data(item=item, purchase=database.Purchase(
        item_id=item_id,
        buyer=call.from_user.id,
        purchase_time=datetime.now()
    ))


@dp.message_handler(regexp=r"^(\d+)$", state=ShoesStates.choosing_quantity)
async def entering_quantity(message: types.Message, state: FSMContext):
    quantity = int(message.text)
    async with state.proxy() as data:
        data["purchase"].quantity = quantity
        item = data.get("item")
        amount = item.price * quantity
        data["purchase"].amount = amount
        data["purchase"].text = "<b>{name}</b>\n{price}*{quantity}\nСумма: {amount}".format(name=item.name,
                                                                                            price=item.price,
                                                                                            quantity=quantity,
                                                                                            amount=amount)
    await message.answer(text=_("Товар - {name}\nКоличество - {quantity}\nСумма - {amount}").format(name=item.name,
                                                                                                    quantity=quantity,
                                                                                                    amount=amount))
    await message.answer(text=_("Согласитесь на покупку!"), reply_markup=agree)
    await ShoesStates.confirm_buying.set()


@dp.callback_query_handler(text_contains="cancel", state=ShoesStates.confirm_buying)
async def cancel_buying(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.reset_state()
    await call.message.answer(text=_("Вы отменили покупку!"))
    await call.message.answer(text=_("Что вы хотите купить?"), reply_markup=shoes)
    await ShoesStates.choosing_type.set()


@dp.callback_query_handler(text_contains="agree", state=ShoesStates.confirm_buying)
async def cancel_buying(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    purchase = data.get("purchase")
    await purchase.create()
    await call.message.answer(text=_("Товар успешно добавлено в корзину."))
    await call.message.answer(text=_("Ещё что хотите купить?"), reply_markup=shoes)
    await ShoesStates.choosing_type.set()


@dp.callback_query_handler(deleting_item.filter(), state=ShoesStates.choosing_shoes)
async def delete_item(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.reset_state()
    item_id = int(callback_data.get("item_id"))
    try:
        await db.delete_item(item_id=item_id)
    except Exception:
        await call.message.answer(text=_("<b><i>Не удалось удалить товар!</i></b>"), reply_markup=shoes)
        await ShoesStates.choosing_type.set()
        return
    await call.message.answer(text=_("Товар успешно удален"), reply_markup=shoes)
    await ShoesStates.choosing_type.set()
