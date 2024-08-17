from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from database.db_main import Database
from dialogs.router import router
from keyboards.base import BaseKeyboard
from lexicon.buttons import SearchButtonsTexts
from lexicon.texts import ProfileTexts
from states.menu import MenuStates
from states.search import SearchTeammateStates


async def like_found_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')
    liked_user: int = dialog_manager.dialog_data.get('this_found_user')

    this_user: dict = await database.users.update_user_watched_users(
        user_id=callback.from_user.id,
        new_watched_user=liked_user
    )

    await dialog_manager.event.bot.send_photo(
        chat_id=liked_user,
        caption=ProfileTexts.send_message_to_liked_user.format(
            **this_user
        ),
        photo=this_user['photo'].file_id.file_id,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=SearchButtonsTexts.send,
                    url=callback.from_user.url
                )],
                *await BaseKeyboard.back_to_menu().render_keyboard(
                    data={},
                    manager=dialog_manager
                )
            ]
        )
    )


async def dislike_found_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    database: Database = dialog_manager.middleware_data.get('database')
    disliked_user = dialog_manager.dialog_data.get('this_found_user')

    await database.users.update_user_watched_users(
        user_id=callback.from_user.id,
        new_watched_user=disliked_user
    )
