from aiogram.dispatcher.filters.state import StatesGroup, State


class ShoesStates(StatesGroup):
    choosing_type = State()
    choosing_shoes = State()
    choosing_size = State()
    choosing_quantity = State()
    confirm_buying = State()
