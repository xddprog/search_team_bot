from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import DialogManager, StartMode

from keyboards.base import BaseKeyboard
from lexicon.buttons import SearchButtonsTexts
from lexicon.texts import SearchTexts


async def send_message_to_team_admins(
    admins: list[int],
    this_user: dict,
    user_who_liked_url: str,
    dialog_manager: DialogManager,
    team_id: int,
    team_name: str
) -> None:
    for admin_id in admins:
        await dialog_manager.event.bot.send_photo(
            chat_id=admin_id,
            caption=SearchTexts.send_message_to_liked_team.format(
                name=team_name,
                **this_user
            ),
            photo=this_user['photo'].file_id.file_id,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=SearchButtonsTexts.send,
                            url=user_who_liked_url
                        ),
                        InlineKeyboardButton(
                            text=SearchButtonsTexts.accept_to_team,
                            callback_data=f'accept_user_to_found_team_{this_user['id']}_{team_id}',
                        )
                    ],
                    *await BaseKeyboard.back_to_menu().render_keyboard(
                        data={},
                        manager=dialog_manager
                    )
                ]
            )
        )


async def send_message_to_liked_user(
    dialog_manager: DialogManager,
    this_user: dict,
    liked_user_id: int,
    user_who_liked_url: str
):
    await dialog_manager.event.bot.send_photo(
        chat_id=liked_user_id,
        caption=SearchTexts.send_message_to_liked_user.format(
            **this_user
        ),
        photo=this_user['photo'].file_id.file_id,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=SearchButtonsTexts.send,
                    url=user_who_liked_url
                )],
                *await BaseKeyboard.back_to_menu().render_keyboard(
                    data={},
                    manager=dialog_manager
                )
            ]
        )
    )
