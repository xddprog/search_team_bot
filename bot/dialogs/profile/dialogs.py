from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, Column
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from filters.user_profile_filters import username_filter, age_filter, city_filter, description_filter
from keyboards.base import BaseKeyboard
from utils.enums import Languages
from .getters import get_user_profile, get_editable_data
from states.profile import ProfileStates, EditProfileStates, DeleteProfileStates
from lexicon.texts import ProfileTexts, EditProfileTexts, DeleteProfileTexts
from lexicon.buttons import ProfileButtonsTexts, EditProfileButtonsTexts, BaseButtonsTexts
from .handlers import (
    go_to_edit_profile, set_editable_item,
    correct_input_handler, invalid_input_handler,
    set_sex, set_photo, set_languages, save_editable_data,
    delete_profile, go_to_register, go_to_delete_profile,
    go_to_user_teams,
)

main_profile_dialog = Dialog(
    Window(
        Format(ProfileTexts.profile),
        DynamicMedia("photo"),
        Column(
            Button(
                id='edit_profile',
                text=Const(ProfileButtonsTexts.edit_profile),
                on_click=go_to_edit_profile
            ),
            Button(
                id='delete_profile',
                text=Const(ProfileButtonsTexts.delete_profile),
                on_click=go_to_delete_profile
            ),
            Button(
                id='teams',
                text=Const(ProfileButtonsTexts.user_teams),
                on_click=go_to_user_teams
            ),
            BaseKeyboard.back_to_menu()
        ),
        state=ProfileStates.profile,
        getter=get_user_profile
    )
)


edit_profile_dialog = Dialog(
    Window(
        Format(EditProfileTexts.main),
        Column(
            BaseKeyboard.keyboard_builder(
                on_click=set_editable_item,
                texts=EditProfileButtonsTexts,
            ),
            Button(
                id='save',
                text=Const(BaseButtonsTexts.save),
                on_click=save_editable_data,
                when='editable_data',
            ),
            BaseKeyboard.back_and_done()
        ),
        state=EditProfileStates.main,
        getter=get_editable_data
    ),
    Window(
        Const(EditProfileTexts.username),
        BaseKeyboard.back_to(EditProfileStates.main),
        TextInput(
            id='username',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=username_filter
        ),
        state=EditProfileStates.edit_username
    ),
    Window(
        Const(EditProfileTexts.age),
        BaseKeyboard.back_to(EditProfileStates.main),
        TextInput(
            id='age',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=age_filter
        ),
        state=EditProfileStates.edit_age
    ),
    Window(
        Const(EditProfileTexts.sex),
        BaseKeyboard.sex_keyboard(on_click=set_sex),
        BaseKeyboard.back_to(EditProfileStates.main),
        state=EditProfileStates.edit_sex
    ),
    Window(
        Const(EditProfileTexts.city),
        BaseKeyboard.back_to(EditProfileStates.main),
        TextInput(
            id='city',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=city_filter
        ),
        state=EditProfileStates.edit_city
    ),
    Window(
        Const(EditProfileTexts.languages),
        BaseKeyboard.checkbox_keyboard(Languages, 'languages'),
        BaseKeyboard.back_to(EditProfileStates.main),
        Button(
            id='languages',
            text=Const(BaseButtonsTexts.save),
            on_click=set_languages
        ),
        state=EditProfileStates.edit_languages,
    ),
    Window(
        Const(EditProfileTexts.user_description),
        BaseKeyboard.back_to(EditProfileStates.main),
        TextInput(
            id='user_description',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=description_filter
        ),
        state=EditProfileStates.edit_description
    ),
    Window(
        Const(EditProfileTexts.photo),
        BaseKeyboard.back_to(EditProfileStates.main),
        MessageInput(
            func=set_photo,
            content_types=ContentType.PHOTO
        ),
        state=EditProfileStates.edit_photo
    )
)


delete_profile_dialog = Dialog(
    Window(
        Const(DeleteProfileTexts.delete),
        Row(
            Button(
                id='accept_delete',
                text=Const(BaseButtonsTexts.yes),
                on_click=delete_profile
            ),
            BaseKeyboard.back_and_done()
        ),
        state=DeleteProfileStates.delete
    ),
    Window(
        Const(DeleteProfileTexts.accept),
        Button(
            id='delete_successfully',
            text=Const(BaseButtonsTexts.register),
            on_click=go_to_register
        ),
        state=DeleteProfileStates.accept
    )
)
