from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from database.db_main import Database
from states.profile import ProfileStates
from states.search import SearchTeammateStates, SearchTeamStates


async def go_to_profile_dialog(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.start(state=ProfileStates.profile, mode=StartMode.RESET_STACK)


async def go_to_search_teammate_dialog(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=SearchTeammateStates.search, mode=StartMode.RESET_STACK)


async def go_to_search_team_dialog(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=SearchTeamStates.main, mode=StartMode.RESET_STACK)
