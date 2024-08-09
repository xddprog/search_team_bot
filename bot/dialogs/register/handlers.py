from pprint import pprint

from aiogram import Router
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, ManagedCheckbox

from database.db_main import Database
from dialogs.router import router
from states.menu import MenuStates
from states.register import RegisterStates


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


async def set_sex(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    dialog_manager.dialog_data.update({'sex': callback.data})
    await dialog_manager.next()


async def set_languages(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    field_name = button.widget_id
    dialog_manager.dialog_data.update({field_name: dialog_manager.dialog_data.get('languages')})
    await dialog_manager.next()


async def set_photo(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager
) -> None:
    file_id = message.photo[0].file_id
    dialog_manager.dialog_data.update({'photo': file_id, 'id': message.from_user.id})

    dialog_data = dialog_manager.dialog_data

    database: Database = dialog_manager.middleware_data.get('database')
    await database.users.add_item(**dialog_data)

    await dialog_manager.next()


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager, database: Database):
    user = await database.users.get_item(message.from_user.id)
    if user:
        # await dialog_manager.start(state=RegisterStates.error, mode=StartMode.RESET_STACK)
        await dialog_manager.start(state=MenuStates.main, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(state=RegisterStates.username, mode=StartMode.RESET_STACK)
