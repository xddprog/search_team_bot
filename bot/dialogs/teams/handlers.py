from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button

from database.db_main import Database
from lexicon.texts import DeleteTeamTexts
from states.teams import CreateTeamStates, ViewTeamStates, AcceptInviteToTeamStates, EditTeamStates, DeleteTeamStates, \
    UserTeamsStates, ViewTeamUserStates, RemoveTeamUserStates


async def edit_team_correct_input_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:
    field_name = widget.widget.widget_id
    dialog_manager.dialog_data.update({field_name: text})
    print(dialog_manager.dialog_data)
    await dialog_manager.switch_to(state=EditTeamStates.main)


async def invalid_input_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError
) -> None:
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    await message.answer(text=str(error))


async def create_team_correct_input_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:
    field_name = widget.widget.widget_id
    dialog_manager.dialog_data.update({field_name: text})
    print(dialog_manager.dialog_data)
    await dialog_manager.next()


async def create_team_set_languages(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    field_name = button.widget_id
    dialog_manager.dialog_data.update({'languages': dialog_manager.dialog_data.get('languages')})
    await dialog_manager.next()


async def edit_team_set_languages(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    field_name = button.widget_id
    dialog_manager.dialog_data.update({'languages': dialog_manager.dialog_data.get('languages')})
    await dialog_manager.switch_to(state=EditTeamStates.main)


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


async def set_edit_photo(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager
) -> None:
    file_id = message.photo[0].file_id
    dialog_manager.dialog_data.update({'photo': file_id})
    await dialog_manager.switch_to(state=EditTeamStates.main)


async def go_to_selected_user_team(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    item: str
) -> None:
    await dialog_manager.start(
        state=ViewTeamStates.team,
        data={'selected_user_team': eval(item)}
    )


async def go_to_selected_team_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    item: str
) -> None:
    await dialog_manager.start(
        state=ViewTeamUserStates.view_user,
        data={
            'selected_user_team': dialog_manager.start_data.get('selected_user_team'),
            'selected_team_user': eval(item),
            'admins': dialog_manager.dialog_data.get('admins')
        }
    )
    await dialog_manager.back()


async def go_to_delete_team(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        state=DeleteTeamStates.delete,
        data={'selected_user_team': dialog_manager.start_data.get('selected_user_team')}
    )


async def go_to_create_team(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=CreateTeamStates.name, mode=StartMode.RESET_STACK)


async def go_to_teams(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        state=UserTeamsStates.teams,
        mode=StartMode.RESET_STACK
    )


async def go_to_team_info_after_remove_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        state=ViewTeamStates.team,
        data={'selected_user_team': dialog_manager.start_data.get('selected_user_team')}
    )


async def go_to_remove_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        state=RemoveTeamUserStates.remove,
        data={
            'selected_user_team': dialog_manager.start_data.get('selected_user_team'),
            'selected_team_user': dialog_manager.start_data.get('selected_team_user')
        }
    )


async def go_to_edit_team(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        state=EditTeamStates.main,
        data={'selected_user_team': dialog_manager.start_data.get('selected_user_team')}
    )


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


async def set_editable_item(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.switch_to(state=EditTeamStates.__dict__.get(button.widget_id))


async def save_editable_data(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')

    await database.teams.update_item(
        dialog_manager.start_data.get('selected_user_team')[-1],
        dialog_manager.dialog_data
    )

    await dialog_manager.done()


async def delete_team(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')
    selected_user_team = dialog_manager.start_data.get('selected_user_team')

    users = await database.teams.delete_item(selected_user_team[-1])
    users.remove(callback.from_user.id)

    for user in users:
        await dialog_manager.event.bot.send_message(
            chat_id=user,
            text=DeleteTeamTexts.message_to_user_deleted_team.format(selected_user_team[0])
        )

    await dialog_manager.next()


async def delete_team_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    print(dialog_manager.start_data)
    database: Database = dialog_manager.middleware_data.get('database')
    selected_team_user_id = dialog_manager.start_data.get('selected_team_user')[0]
    selected_user_team_id = dialog_manager.start_data.get('selected_user_team')[-1]

    user = await database.users.get_item(selected_team_user_id)
    await database.teams.remove_user(selected_user_team_id, user)

    await dialog_manager.next()
