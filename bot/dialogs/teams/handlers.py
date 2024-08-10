import json

from aiogram.filters import CommandStart, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import decode_payload
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button

from database.db_main import Database
from dialogs.router import router
from states.teams import CreateTeamStates, ViewTeamStates, AcceptInviteToTeamStates


async def correct_input_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:
    field_name = widget.widget.widget_id
    dialog_manager.dialog_data.update({field_name: text})
    await dialog_manager.next()


async def invalid_input_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError
) -> None:
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    await message.answer(text=str(error))


async def set_languages(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    field_name = button.widget_id
    dialog_manager.dialog_data.update({'languages': dialog_manager.dialog_data.get('languages')})
    await dialog_manager.next()


async def set_photo(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')

    dialog_manager.dialog_data.update(
        {
            'photo': message.photo[0].file_id,
            'admins': [message.from_user.id],
            'users': [await database.users.get_item(message.from_user.id)]
        }
    )

    await database.teams.add_item(**dialog_manager.dialog_data)

    await dialog_manager.next()


async def go_to_selected_user_team(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    item: list
) -> None:
    await dialog_manager.start(
        state=ViewTeamStates.team,
        mode=StartMode.RESET_STACK,
        data={'selected_user_team': eval(item)}
    )


async def go_to_create_team(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=CreateTeamStates.name, mode=StartMode.RESET_STACK)


async def create_invite_to_team_link(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager
) -> None:
    selected_team_name, selected_team_id = dialog_manager.start_data.get('selected_user_team')

    link = await create_start_link(
        callback.bot,
        f'invite_to_team_{selected_team_id}_{selected_team_name}',
        encode=True
    )
    dialog_manager.dialog_data.update({'invite_to_team_link': link})

    await dialog_manager.switch_to(ViewTeamStates.invite)


async def accept_invite_to_team(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')

    user = await database.users.get_item(callback.from_user.id)
    team_id = dialog_manager.start_data.get('team_id')

    await database.teams.add_user_to_team(team_id, user)

    await dialog_manager.start(AcceptInviteToTeamStates.accept_invite, mode=StartMode.RESET_STACK)