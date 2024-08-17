from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Column, Row, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from keyboards.base import BaseKeyboard
from .getters import get_found_user_info
from .handlers import like_found_user, dislike_found_user
from lexicon.buttons import SearchButtonsTexts
from lexicon.texts import ProfileTexts
from states.search import SearchTeammateStates

search_teammate_dialog = Dialog(
    Window(
        Format(ProfileTexts.profile),
        DynamicMedia("photo"),
        Column(
            Row(
                Button(
                    id='like_found_user',
                    text=Const(SearchButtonsTexts.like),
                    on_click=like_found_user
                ),
                Button(
                    id='dislike_found_user',
                    text=Const(SearchButtonsTexts.dislike),
                    on_click=dislike_found_user
                ),
                BaseKeyboard.back_to_menu()
            ),
        ),
        state=SearchTeammateStates.search,
        getter=get_found_user_info
    )
)


search_team_dialog = Dialog(
    Window(
        state=SearchTeammateStates.search
    )
)