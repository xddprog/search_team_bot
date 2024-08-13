from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Column, Row, Button
from aiogram_dialog.widgets.text import Format, Const

from keyboards.base import BaseKeyboard
from .handlers import like_found_user, dislike_found_user, skip_found_user
from lexicon.buttons import SearchButtonsTexts
from lexicon.texts import ProfileTexts
from states.search import SearchTeammateStates

search_teammate_dialog = Dialog(
    Window(
        Format(ProfileTexts.profile),
        Column(
            Row(
                Button(
                    id='like_found_user',
                    text=Const(SearchButtonsTexts.like),
                    on_click=like_found_user
                ),
                Button(
                    id='dislike_found_user',
                    text=Const(SearchButtonsTexts.like),
                    on_click=dislike_found_user
                ),
                Button(
                    id='skip_found_user',
                    text=Const(SearchButtonsTexts.like),
                    on_click=skip_found_user
                ),
            ),
            BaseKeyboard.back_to_menu()
        ),
        state=SearchTeammateStates.search,
        getter=get_found_user_info
    )
)