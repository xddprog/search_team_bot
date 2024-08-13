from aiogram.fsm.state import StatesGroup, State


class SearchTeammateStates(StatesGroup):
    search = State()


class SearchTeam(StatesGroup):
    main = State()
