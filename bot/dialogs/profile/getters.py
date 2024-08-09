from aiogram.enums import ContentType
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Context, MediaAttachment, MediaId

from database.db_main import Database
from lexicon.buttons import EditProfileButtonsTexts
from lexicon.texts import EditProfileTexts, BaseProfileInputTexts, ProfileItemsTexts


async def get_user_profile(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs
) -> dict:
    database: Database = dialog_manager.middleware_data.get('database')

    user = await database.users.get_item(event_from_user.id)

    return await user.to_dict()


async def get_editable_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    editable_data = [
        f'<b>{ProfileItemsTexts.__dict__[key]}</b>: {value}'
        for key, value in dialog_manager.dialog_data.items()
    ]

    return {
        'editable_data': ',\n'.join(editable_data)
    }