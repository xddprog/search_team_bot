from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Select, Button, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from filters.register_filters import username_filter, description_filter
from keyboards.base import BaseKeyboard
from lexicon.buttons import CreateEditDeleteAddButtonsTexts, BaseButtonsTexts, ViewTeamButtonsTexts
from utils.enums import Languages
from .getters import get_user_teams, get_team_register_fields, get_team_info, get_invite_to_team_link, \
    get_team_info_from_invite_link
from lexicon.texts import TeamsTexts, BaseInputTexts, AcceptToInviteTeamDialogs
from states.teams import UserTeamsStates, CreateTeamStates, ViewTeamStates, AcceptInviteToTeamStates
from .handlers import (
    go_to_selected_user_team, go_to_create_team,
    invalid_input_handler, correct_input_handler,
    set_languages, set_photo, create_invite_to_team_link,
    accept_invite_to_team
)


user_teams_dialog = Dialog(
    Window(
        Format(TeamsTexts.teams),
        Select(
            Format('{item[0]}'),
            id='user_team',
            item_id_getter=lambda team: team,
            items='teams',
            on_click=go_to_selected_user_team
        ),
        Button(
            id='create_team',
            text=Const(CreateEditDeleteAddButtonsTexts.create),
            on_click=go_to_create_team,
            when='teams_numbers_no_more_limit'
        ),
        BaseKeyboard.back_and_done(),
        getter=get_user_teams,
        state=UserTeamsStates.teams
    )
)

create_team_dialog = Dialog(
    Window(
        Const(BaseInputTexts.name),
        BaseKeyboard.back_and_done(),
        TextInput(
            id='name',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=username_filter
        ),
        state=CreateTeamStates.name
    ),
    Window(
        Const(BaseInputTexts.team_description),
        BaseKeyboard.back_and_done(),
        TextInput(
            id='description',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=description_filter
        ),
        state=CreateTeamStates.description
    ),
    Window(
        Const(BaseInputTexts.languages),
        BaseKeyboard.checkbox_keyboard(Languages, 'languages'),
        BaseKeyboard.back_and_done(),
        Button(
            id='languages',
            text=Const(BaseButtonsTexts.save),
            on_click=set_languages
        ),
        state=CreateTeamStates.languages,
    ),
    Window(
        Const(BaseInputTexts.photo),
        BaseKeyboard.back_and_done(),
        MessageInput(
            func=set_photo,
            content_types=ContentType.PHOTO
        ),
        state=CreateTeamStates.photo
    ),
    Window(
        Format(TeamsTexts.success),
        BaseKeyboard.back_and_done(),
        DynamicMedia("photo"),
        state=CreateTeamStates.success,
        getter=get_team_register_fields
    )
)


view_team_dialog = Dialog(
    Window(
        Format(TeamsTexts.team),
        DynamicMedia("photo"),
        Button(
            id='leave',
            text=Const(ViewTeamButtonsTexts.edit),
            when='user_is_not_admin'
        ),
        Button(
            id='edit_team',
            text=Const(ViewTeamButtonsTexts.edit),
            when='user_is_admin'
        ),
        Button(
            id='invite',
            text=Const(ViewTeamButtonsTexts.invite),
            on_click=create_invite_to_team_link
        ),
        Button(
            id='users',
            text=Const(ViewTeamButtonsTexts.users)
        ),
        state=ViewTeamStates.team,
        getter=get_team_info
    ),
    Window(
        Format(TeamsTexts.invite_link),
        BaseKeyboard.back(),
        state=ViewTeamStates.invite,
        getter=get_invite_to_team_link
    )
)


accept_invite_to_team_dialog = Dialog(
    Window(
        Format(AcceptToInviteTeamDialogs.invite),
        Row(
            Button(
                id='invite',
                text=Const(BaseButtonsTexts.yes),
                on_click=accept_invite_to_team
            ),
            BaseKeyboard.back_to_menu()
        ),
        state=AcceptInviteToTeamStates.invite,
        getter=get_team_info_from_invite_link
    ),
    Window(
        Format(AcceptToInviteTeamDialogs.success_accept_invite_to_team),
        BaseKeyboard.back_to_menu(),
        state=AcceptInviteToTeamStates.accept_invite,
        getter=get_team_info_from_invite_link
    ),
    Window(
        Const(AcceptToInviteTeamDialogs.accept_invite_error),
        BaseKeyboard.back_to_menu(),
        state=AcceptInviteToTeamStates.accept_invite_error
    )
)