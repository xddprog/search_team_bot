from aiogram.types import User
from aiogram_dialog import DialogManager, StartMode

from database.db_main import Database
from database.models import UserModel
from states.search import SearchTeammateStates, SearchTeamStates


async def get_found_user_info(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs
) -> dict:
    found_user: UserModel = dialog_manager.start_data.get('found_user')
    return found_user


async def get_found_team_info(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs
) -> dict:
    found_team: UserModel = dialog_manager.start_data.get('found_team')
    return found_team
