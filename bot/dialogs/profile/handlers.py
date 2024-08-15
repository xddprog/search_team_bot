from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from database.db_main import Database
from states.profile import EditProfileStates, ProfileStates, DeleteProfileStates
from states.register import RegisterStates
from states.teams import UserTeamsStates


async def go_to_edit_profile(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=EditProfileStates.main)


async def go_to_delete_profile(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=DeleteProfileStates.delete)


async def go_to_user_teams(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=UserTeamsStates.teams)


async def correct_input_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:
    field_name = widget.widget.widget_id
    dialog_manager.dialog_data.update({field_name: text})
    await dialog_manager.switch_to(state=EditProfileStates.main)


async def invalid_input_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError
) -> None:
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    await message.answer(text=str(error))


async def set_sex(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    dialog_manager.dialog_data.update({'sex': button.text})
    await dialog_manager.switch_to(state=EditProfileStates.main)


async def set_photo(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager
) -> None:
    file_id = message.photo[0].file_id
    dialog_manager.dialog_data.update({'photo': file_id})
    await dialog_manager.switch_to(state=EditProfileStates.main)


async def set_languages(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    field_name = button.widget_id
    dialog_manager.dialog_data.update({field_name: dialog_manager.dialog_data.get('languages')})
    await dialog_manager.switch_to(state=EditProfileStates.main)


async def set_editable_item(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.switch_to(state=EditProfileStates.__dict__.get(button.widget_id))


async def save_editable_data(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')

    await database.users.update_item(callback.from_user.id, dialog_manager.dialog_data)

    await dialog_manager.done()


async def delete_profile(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')

    await database.users.delete_item(callback.from_user.id)

    await dialog_manager.next()


async def go_to_register(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(RegisterStates.username, mode=StartMode.RESET_STACK)
