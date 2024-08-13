from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def like_found_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    pass


async def dislike_found_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    pass


async def skip_found_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    pass
