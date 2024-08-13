from aiogram.types import User
from aiogram_dialog import DialogManager

from database.db_main import Database
from database.models import UserModel


async def get_found_user_info(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs
) -> dict:
    database: Database = await dialog_manager.middleware_data.get('database')
    found_users: list[UserModel] | None = dialog_manager.dialog_data.get('found_users')

    if not found_users:
        found_users = await database.users.get_users_for_search_dialog(
            user_id=event_from_user.id,
            offset=dialog_manager.dialog_data.get('offset', 0)
        )

        dialog_manager.dialog_data['found_users'] = found_users
        dialog_manager.dialog_data['offset'] = dialog_manager.dialog_data.get('offset', 0) + 5

    return found_users.pop().to_dict()
