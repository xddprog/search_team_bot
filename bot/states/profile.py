from aiogram.fsm.state import StatesGroup, State


class ProfileStates(StatesGroup):
    profile = State()


class EditProfileStates(StatesGroup):
    main = State()
    edit_username = State()
    edit_age = State()
    edit_sex = State()
    edit_city = State()
    edit_description = State()
    edit_languages = State()
    edit_photo = State()


class DeleteProfileStates(StatesGroup):
    delete = State()
    accept = State()