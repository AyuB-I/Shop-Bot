from aiogram.dispatcher.filters.state import StatesGroup, State


class NewItemStates(StatesGroup):
    name = State()
    category = State()
    photo = State()
    price = State()
    confirm = State()
    added = State()


class MailingStates(StatesGroup):
    mailing = State()
    mailing_confirm = State()
