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
    database: Database = dialog_manager.middleware_data.get('database')

    found_user = await database.users.get_users_for_search_dialog(
        user_id=callback.from_user.id
    )

    if not found_user:
        await dialog_manager.start(state=SearchTeammateStates.users_ended)
    else:
        found_user = await found_user.to_dict()
        await database.users.update_user_watched_users(
            user_id=callback.from_user.id,
            new_watched_user=found_user['id']
        )
        await dialog_manager.start(
            state=SearchTeammateStates.search,
            mode=StartMode.RESET_STACK,
            data={'found_user': found_user}
        )


async def go_to_search_team_dialog(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')

    found_team = await database.teams.get_teams_for_search_dialog(
        this_user=await database.users.get_item(callback.from_user.id)
    )

    if not found_team:
        await dialog_manager.start(state=SearchTeamStates.teams_ended)
    else:
        await database.users.update_user_watched_teams(
            user_id=callback.from_user.id,
            new_watched_team=found_team.id
        )
        await dialog_manager.start(
            state=SearchTeamStates.search,
            mode=StartMode.RESET_STACK,
            data={'found_team': await found_team.to_dict()}
        )
