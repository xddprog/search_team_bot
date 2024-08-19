from aiogram.enums import ContentType
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Context, MediaAttachment, MediaId

from database.db_main import Database
from lexicon.texts import ProfileAndTeamItemsTexts


async def get_user_teams(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs
) -> dict:
    database: Database = dialog_manager.middleware_data.get('database')

    user = await database.users.get_item(event_from_user.id)

    return {
        'teams_numbers': len(user.teams),
        'teams_numbers_no_more_limit': len(user.teams) < 10,
        'teams': [(team.name, team.id) for team in user.teams]
    }


async def get_team_register_fields(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    dialog_data = dialog_manager.dialog_data

    dialog_data['photo'] = MediaAttachment(
        ContentType.PHOTO,
        file_id=MediaId(file_id=dialog_data.get('photo'))
    )
    dialog_data['languages'] = ', '.join(dialog_data.get('languages'))

    return dialog_data


async def get_team_info(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs
) -> dict:
    database: Database = dialog_manager.middleware_data.get('database')

    team = await database.teams.get_item(dialog_manager.start_data.get('selected_user_team')[-1])
    team = await team.to_dict()

    team['user_is_admin'] = event_from_user.id in team['admins']
    team['user_is_not_admin'] = event_from_user.id not in team['admins']

    dialog_manager.dialog_data['users'] = team['users']
    dialog_manager.dialog_data['admins'] = team['admins']

    return team


async def get_invite_to_team_link(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    invite_to_team_link = dialog_manager.dialog_data.pop('invite_to_team_link')
    return {
        'invite_to_team_link': invite_to_team_link
    }


async def get_team_info_from_invite_link(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return dialog_manager.start_data


async def get_editable_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    editable_data = [
        f'<b>{ProfileAndTeamItemsTexts.__dict__[key]}</b>: {value}'
        for key, value in dialog_manager.dialog_data.items()
    ]

    return {
        'editable_data': ',\n'.join(editable_data)
    }


async def get_team_users(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    users = dialog_manager.dialog_data.get('users')

    return {
        'users': users,
        'team_users_number': len(users)
    }


async def get_selected_user_info(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    database: Database = dialog_manager.middleware_data.get('database')
    selected_user_info_id = dialog_manager.start_data.get('selected_team_user')[0]
    team_admins = dialog_manager.start_data.get('admins')

    selected_user_info = await database.users.get_item(selected_user_info_id)
    selected_user_info = await selected_user_info.to_dict()
    selected_user_info['user_is_admin'] = selected_user_info_id in team_admins

    return selected_user_info
