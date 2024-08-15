from aiogram.types import User
from aiogram_dialog import DialogManager

from database.db_main import Database
from database.models import UserModel
from states.search import SearchTeammateStates


async def get_found_user_info(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs
) -> dict:
    database: Database = dialog_manager.middleware_data.get('database')
    found_users: list[UserModel] | None = dialog_manager.dialog_data.get('found_users')

    if found_users:
        this_found_user = found_users.pop()

        dialog_manager.dialog_data['this_found_user'] = this_found_user.id

        return await this_found_user.to_dict()

    new_found_users = await database.users.get_users_for_search_dialog(
        user_id=event_from_user.id,
        offset=dialog_manager.dialog_data.get('offset', 0)
    )

    if new_found_users:
        dialog_manager.dialog_data['found_users'] = new_found_users
        dialog_manager.dialog_data['offset'] = dialog_manager.dialog_data.get('offset', 0) + 5

        this_found_user = new_found_users.pop()
        dialog_manager.dialog_data['this_found_user'] = this_found_user.id

        return await this_found_user.to_dict()
    return await dialog_manager.switch_to(state=SearchTeammateStates.users_not_found)

