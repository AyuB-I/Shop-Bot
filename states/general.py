from aiogram.dispatcher.filters.state import StatesGroup, State


class GeneralStates(StatesGroup):
    shoes = State()
    settings = State()


class SettingStates(StatesGroup):
    getting_language = State()