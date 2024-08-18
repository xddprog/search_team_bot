from aiogram.fsm.state import StatesGroup, State


class SearchTeammateStates(StatesGroup):
    search = State()
    users_ended = State()


class SearchTeamStates(StatesGroup):
    search = State()
    teams_ended = State()
