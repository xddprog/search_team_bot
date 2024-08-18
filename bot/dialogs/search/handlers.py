from aiogram import F, Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from database.db_main import Database
from dialogs.router import router
from lexicon.texts import SearchTexts
from states.search import SearchTeammateStates, SearchTeamStates
from utils.func import send_message_to_team_admins, send_message_to_liked_user


async def like_found_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')
    liked_user: dict = dialog_manager.start_data.get('found_user')

    this_user: dict = await database.users.update_user_watched_users(
        user_id=callback.from_user.id,
        new_watched_user=liked_user['id']
    )

    await send_message_to_liked_user(
        dialog_manager=dialog_manager,
        this_user=this_user,
        user_who_liked_url=callback.from_user.url,
        liked_user_id=liked_user['id']
    )

    next_user = await database.users.get_users_for_search_dialog(
        user_id=callback.from_user.id
    )

    if next_user is None:
        return await dialog_manager.switch_to(state=SearchTeammateStates.users_ended)
    else:
        dialog_manager.start_data['found_user'] = await next_user.to_dict()


async def dislike_found_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')
    disliked_user: dict = dialog_manager.start_data.get('found_user')

    await database.users.update_user_watched_users(
        user_id=callback.from_user.id,
        new_watched_user=disliked_user['id']
    )

    next_user = await database.users.get_users_for_search_dialog(
        user_id=callback.from_user.id
    )

    if next_user is None:
        return await dialog_manager.switch_to(state=SearchTeammateStates.users_ended)
    else:
        dialog_manager.start_data['found_user'] = await next_user.to_dict()


async def like_found_team(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')
    liked_team: dict = dialog_manager.start_data.get('found_team')

    this_user: dict = await database.users.update_user_watched_teams(
        user_id=callback.from_user.id,
        new_watched_team=liked_team['id']
    )

    await send_message_to_team_admins(
        admins=liked_team['admins'],
        user_who_liked_url=callback.from_user.url,
        this_user=this_user,
        dialog_manager=dialog_manager,
        team_id=liked_team['id'],
        team_name=liked_team['name']
    )

    next_team = await database.teams.get_teams_for_search_dialog(
        this_user=await database.users.get_item(callback.from_user.id)
    )
    if next_team is None:
        return await dialog_manager.switch_to(state=SearchTeammateStates.users_ended)
    else:
        dialog_manager.start_data['found_team'] = await next_team.to_dict()


async def dislike_found_team(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')
    disliked_team: dict = dialog_manager.start_data.get('found_team')

    await database.users.update_user_watched_teams(
        user_id=callback.from_user.id,
        new_watched_team=disliked_team['id']
    )

    next_team = await database.teams.get_teams_for_search_dialog(
        this_user=await database.users.get_item(callback.from_user.id)
    )
    if next_team is None:
        return await dialog_manager.switch_to(state=SearchTeamStates.teams_ended)
    else:
        dialog_manager.start_data['found_team'] = await next_team.to_dict()


@router.callback_query(F.data.startswith('accept_user_to_found_team_'))
async def accept_user_to_found_team(callback: CallbackQuery, database: Database, bot: Bot):
    *_, user_id, team_id = callback.data.split('_')

    team_name = await database.teams.update_team_users(
        team_id=int(team_id),
        new_user=await database.users.get_item(int(user_id))
    )

    await bot.send_message(
        chat_id=int(user_id),
        text=SearchTexts.accept_user_to_team.format(team_name)
    )

    await callback.answer()