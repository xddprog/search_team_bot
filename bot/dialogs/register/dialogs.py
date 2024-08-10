from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from .getters import get_user_register_fields
from .handlers import correct_input_handler, invalid_input_handler, set_sex, set_languages, set_photo
from filters.register_filters import age_filter, username_filter, description_filter, city_filter
from keyboards.base import BaseKeyboard
from lexicon.buttons import BaseButtonsTexts
from lexicon.texts import StartDialogTexts as Texts
from states.register import RegisterStates
from utils.enums import Languages

register_dialog = Dialog(
    Window(
        Const(Texts.username),
        TextInput(
            id='username',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=username_filter
        ),
        state=RegisterStates.username
    ),
    Window(
        Const(Texts.age),
        TextInput(
            id='age',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=age_filter
        ),
        state=RegisterStates.age
    ),
    Window(
        Const(Texts.sex),
        BaseKeyboard.sex_keyboard(on_click=set_sex),
        state=RegisterStates.sex
    ),
    Window(
        Const(Texts.city),
        TextInput(
            id='city',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=city_filter
        ),
        state=RegisterStates.city
    ),
    Window(
        Const(Texts.languages),
        BaseKeyboard.checkbox_keyboard(Languages, 'languages'),
        Button(
            id='languages',
            text=Const(BaseButtonsTexts.save),
            on_click=set_languages
        ),
        state=RegisterStates.languages,
    ),
    Window(
        Const(Texts.user_description),
        TextInput(
            id='user_description',
            on_success=correct_input_handler,
            on_error=invalid_input_handler,
            type_factory=description_filter
        ),
        state=RegisterStates.description
    ),
    Window(
        Const(Texts.photo),
        MessageInput(
            func=set_photo,
            content_types=ContentType.PHOTO
        ),
        state=RegisterStates.photo
    ),
    Window(
        Format(Texts.success),
        BaseKeyboard.back_to_menu(),
        DynamicMedia("photo"),
        state=RegisterStates.success,
        getter=get_user_register_fields
    )
)
