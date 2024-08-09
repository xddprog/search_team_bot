from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const

from .handlers import go_to_profile_dialog, go_to_search_teammate_dialog, go_to_search_team_dialog
from lexicon.buttons import MainMenuButtonsTexts as ButtonTexts
from lexicon.texts import MainMenuTexts as Texts
from states.menu import MenuStates

menu_dialog = Dialog(
    Window(
        Const(Texts.main),
        Column(
            Button(
                id='go_to_profile',
                text=Const(ButtonTexts.profile),
                on_click=go_to_profile_dialog
            ),
            Button(
                id='go_to_search_teammate',
                text=Const(ButtonTexts.search_teammate),
                on_click=go_to_search_teammate_dialog
            ),
            Button(
                id='go_to_search_team',
                text=Const(ButtonTexts.search_team),
                on_click=go_to_search_team_dialog
            )
        ),
        state=MenuStates.main
    )
)
