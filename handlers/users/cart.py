from database import Item, Purchase
from keyboards.defualt import home_page
from loader import dp, _, bot
from aiogram import types
from database import Purchase, Item


@dp.message_handler(text=_("Корзина\U0001F6D2"), state="*")
async def cart(message: types.Message):
    await message.answer(_("<b>У вас в корзине:</b>\n\n"))
    ls = []
    for x in await Purchase.select("id").where(Purchase.buyer == message.from_user.id).gino.all():
        ls.append(x)
    print(ls)



"""
@dp.message_handler(text=_("Корзина\U0001F6D2"), state="*")
async def cart(message: types.Message):
    await message.answer(_("У вас в корзине:\n\n"))
    for text in await Purchase.select("text").where(Purchase.buyer == message.from_user.id).gino.all():
        await message.answer("{text}".format(text="".join(text)))
"""

"""item_id = await Purchase.select("item_id").where(Purchase.id == purchase_id).gino.first()
item = await Item.query.where(Item.id == item_id).gino.all()
purchase = await Purchase.query.where(Purchase.id == purchase_id).gino.all()
text = _("<b>{name}</b>\n{price}*{quantity} = {amount}").format(name=item.name, price=item.price,
                                                                quantity=purchase.quantity,
                                                                amount=purchase.amount)
await message.answer(text=text, reply_markup=home_page)"""
