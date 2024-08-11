from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Select, Button, Row, Column, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from filters.register_filters import username_filter, description_filter
from keyboards.base import BaseKeyboard
from lexicon.buttons import CreateEditDeleteAddButtonsTexts, BaseButtonsTexts, ViewTeamButtonsTexts, \
    EditTeamButtonsTexts, BackButtonsTexts
from utils.enums import Languages
from .getters import get_user_teams, get_team_register_fields, get_team_info, get_invite_to_team_link, \
    get_team_info_from_invite_link, get_editable_data, get_team_users, get_selected_user_info
from lexicon.texts import TeamsTexts, BaseInputTexts, AcceptToInviteTeamDialogs, EditTeamTexts, DeleteTeamTexts, \
    ProfileTexts, RemoveTeamUserTexts
from states.teams import UserTeamsStates, CreateTeamStates, ViewTeamStates, AcceptInviteToTeamStates, EditTeamStates, \
    DeleteTeamStates, ViewTeamUserStates, RemoveTeamUserStates
from .handlers import (
    go_to_selected_user_team, go_to_create_team,
    invalid_input_handler, correct_input_handler,
    set_languages, set_photo, create_invite_to_team_link,
    accept_invite_to_team, set_editable_item, save_editable_data, delete_team, go_to_delete_team, go_to_teams,
    go_to_selected_team_user, go_to_remove_user, delete_team_user, go_to_team_info_after_remove_user
)


user_teams_dialog = Dialog(
    Window(
        Format(TeamsTexts.teams),
        Column(
            Select(
                Format('{item[0]}'),
                id='user_team',
                item_id_getter=lambda team: team,
                items='teams',
                on_click=go_to_selected_user_team
            ),
        ),
        Row(
            Button(
                id='create_team',
                text=Const(CreateEditDeleteAddButtonsTexts.create),
                on_click=go_to_create_team,
                when='teams_numbers_no_more_limit'
            ),
            BaseKeyboard.back_and_done(),
        ),
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
            id='team_description',
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
        Button(
            id='go_to_teams',
            text=Const(BackButtonsTexts.back),
            on_click=go_to_teams
        ),
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
            id='delete_team',
            text=Const(ViewTeamButtonsTexts.delete),
            when='user_is_admin',
            on_click=go_to_delete_team
        ),
        Button(
            id='invite',
            text=Const(ViewTeamButtonsTexts.invite),
            on_click=create_invite_to_team_link
        ),
        SwitchTo(
            id='users',
            text=Const(ViewTeamButtonsTexts.users),
            state=ViewTeamStates.users
        ),
        BaseKeyboard.back_and_done(),
        state=ViewTeamStates.team,
        getter=get_team_info
    ),
    Window(
        Format(TeamsTexts.invite_link),
        BaseKeyboard.back(),
        state=ViewTeamStates.invite,
        getter=get_invite_to_team_link
    ),
    Window(
        Format(TeamsTexts.users),
        Column(
            Select(
                Format('{item[1]}'),
                id='team_user',
                item_id_getter=lambda user: user,
                items='users',
                on_click=go_to_selected_team_user
            )
        ),
        BaseKeyboard.back_to(state=ViewTeamStates.team),
        state=ViewTeamStates.users,
        getter=get_team_users
    )
)


view_team_user_dialog = Dialog(
    Window(
        Format(ProfileTexts.profile),
        DynamicMedia("photo"),
        Button(
            id='remove_user',
            text=Const(ViewTeamButtonsTexts.remove),
            on_click=go_to_remove_user
        ),
        BaseKeyboard.back_and_done(),
        state=ViewTeamUserStates.view_user,
        getter=get_selected_user_info
    )
)


remove_team_user_dialog = Dialog(
    Window(
        Const(RemoveTeamUserTexts.remove),
        Row(
            Button(
                id='accept_delete',
                text=Const(BaseButtonsTexts.yes),
                on_click=delete_team_user
            ),
            BaseKeyboard.back_and_done()
        ),
        state=RemoveTeamUserStates.remove
    ),
    Window(
        Const(RemoveTeamUserTexts.accept),
        Button(
            id='remove_successfully',
            text=Const(BackButtonsTexts.back),
            on_click=go_to_team_info_after_remove_user
        ),
        state=RemoveTeamUserStates.accept
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


edit_team_dialog = Dialog(
    Window(
        Format(EditTeamTexts.main),
        Column(
            BaseKeyboard.keyboard_builder(
                on_click=set_editable_item,
                texts=EditTeamButtonsTexts,
            ),
            Button(
                id='save',
                text=Const(BaseButtonsTexts.save),
                on_click=save_editable_data,
                when='editable_data',
            ),
            BaseKeyboard.back_and_done()
        ),
        state=EditTeamStates.main,
        getter=get_editable_data
    ),
    Window(
        Const(EditTeamStates.edit_name),
        BaseKeyboard.back_to(EditTeamStates.main),
        TextInput(
            id='username',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=username_filter
        ),
        state=EditTeamStates.edit_name
    ),
    Window(
        Const(EditTeamStates.edit_languages),
        BaseKeyboard.checkbox_keyboard(Languages, 'languages'),
        BaseKeyboard.back_to(EditTeamStates.main),
        Button(
            id='languages',
            text=Const(BaseButtonsTexts.save),
            on_click=set_languages
        ),
        state=EditTeamStates.edit_languages,
    ),
    Window(
        Const(EditTeamStates.edit_description),
        BaseKeyboard.back_to(EditTeamStates.main),
        TextInput(
            id='description',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=username_filter
        ),
        state=EditTeamStates.edit_description
    ),
    Window(
        Const(EditTeamTexts.photo),
        BaseKeyboard.back_to(EditTeamStates.main),
        MessageInput(
            func=set_photo,
            content_types=ContentType.PHOTO
        ),
        state=EditTeamStates.edit_photo
    )
)


delete_team_dialog = Dialog(
    Window(
        Const(DeleteTeamTexts.delete),
        Row(
            Button(
                id='accept_delete',
                text=Const(BaseButtonsTexts.yes),
                on_click=delete_team
            ),
            BaseKeyboard.back_and_done()
        ),
        state=DeleteTeamStates.delete
    ),
    Window(
        Const(DeleteTeamStates.accept),
        Button(
            id='delete_successfully',
            text=Const(BackButtonsTexts.back),
            on_click=go_to_teams
        ),
        state=DeleteTeamStates.accept
    )
)
