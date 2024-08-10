from enum import Enum
from typing import Callable

from aiogram.types import BotCommand, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Row, Column, Checkbox, Button, ManagedCheckbox
from aiogram_dialog.widgets.text import Const

from lexicon.buttons import MenuKeyboardTexts, BackButtonsTexts
from states.menu import MenuStates
from utils.enums import SexTypes


class BaseKeyboard:
    @classmethod
    def set_meny_keyboard(cls):
        commands = [
            BotCommand(command=item.name, description=item.value)
            for item in MenuKeyboardTexts
        ]
        return commands

    @classmethod
    def back_to_menu(cls) -> Button:
        return Button(
            id='go_to_menu_button',
            text=Const(BackButtonsTexts.back_to_menu),
            on_click=cls._handle_back_to_menu_button
        )

    @classmethod
    def back_and_done(cls) -> Button:
        return Button(
            id='back_to_teams',
            text=Const(BackButtonsTexts.back),
            on_click=cls._handle_back_and_done_button
        )

    @classmethod
    def back(cls) -> Button:
        return Button(
            id='back_to_teams',
            text=Const(BackButtonsTexts.back),
            on_click=cls._handle_back_button
        )

    @staticmethod
    async def _handle_back_to_menu_button(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
    ) -> None:
        await dialog_manager.start(state=MenuStates.main, show_mode=StartMode.RESET_STACK)

    @staticmethod
    async def _handle_checkbox(
        callback: CallbackQuery,
        checkbox: ManagedCheckbox,
        dialog_manager: DialogManager
    ) -> None:
        field_name, field_value, *_ = callback.data.split('_')
        data = dialog_manager.dialog_data.get(field_name)
        if not data:
            dialog_manager.dialog_data[field_name] = [field_value]
        elif field_value in data:
            dialog_manager.dialog_data[field_name].remove(field_value)
        else:
            dialog_manager.dialog_data[field_name].append(field_value)

    @staticmethod
    async def _handle_back_and_done_button(
        callback: CallbackQuery,
        checkbox: ManagedCheckbox,
        dialog_manager: DialogManager
    ) -> None:
        await dialog_manager.done()

    @staticmethod
    async def _handle_back_button(
            callback: CallbackQuery,
            checkbox: ManagedCheckbox,
            dialog_manager: DialogManager
    ) -> None:
        await dialog_manager.back()

    @classmethod
    def checkbox_keyboard(cls, texts: Enum, field_name: str):
        keyboard = Column(
            *[
                Checkbox(
                    id=f'{field_name}_{text.value}_checkbox',
                    checked_text=Const(f'{text.value} ✅'),
                    unchecked_text=Const(f'{text.value}'),
                    on_state_changed=cls._handle_checkbox
                )
                for text in texts
            ]
        )
        return keyboard

    @staticmethod
    def sex_keyboard(on_click: Callable):
        return Row(
            Button(
                id=str(SexTypes.MALE),
                text=Const(text=str(SexTypes.MALE)),
                on_click=on_click
            ),
            Button(
                id=str(SexTypes.FEMALE),
                text=Const(text=str(SexTypes.MALE)),
                on_click=on_click
            )
        )

    @staticmethod
    def keyboard_builder(
        on_click: Callable,
        texts: Callable,
        start_id_text: str = '',
        is_row: bool = False
    ) -> Row | Column:
        buttons = [
            Button(
                id=f'{start_id_text}{key}',
                text=Const(text=value),
                on_click=on_click
            )
            for key, value in texts().__dict__.items()
        ]

        return Row(*buttons) if is_row else Column(*buttons)