from aiogram.fsm.state import StatesGroup, State


class UserTeamsStates(StatesGroup):
    teams = State()


class CreateTeamStates(StatesGroup):
    name = State()
    description = State()
    languages = State()
    photo = State()
    success = State()


class ViewTeamStates(StatesGroup):
    team = State()
    invite = State()
    users = State()


class ViewTeamUserStates(StatesGroup):
    view_user = State()


class AcceptInviteToTeamStates(StatesGroup):
    accept_invite_error = State()
    invite = State()
    accept_invite = State()


class EditTeamStates(StatesGroup):
    main = State()
    edit_name = State()
    edit_description = State()
    edit_languages = State()
    edit_photo = State()


class DeleteTeamStates(StatesGroup):
    delete = State()
    accept = State()


class RemoveTeamUserStates(StatesGroup):
    remove = State()
    accept = State()
