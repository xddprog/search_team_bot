from aiogram.fsm.state import StatesGroup, State


class SearchTeammateStates(StatesGroup):
    search = State()
    users_not_found = State()


class SearchTeamStates(StatesGroup):
    main = State()
