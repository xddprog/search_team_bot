from aiogram.fsm.state import StatesGroup, State


class RegisterStates(StatesGroup):
    username = State()
    age = State()
    sex = State()
    languages = State()
    city = State()
    description = State()
    photo = State()
    success = State()
    error = State()
