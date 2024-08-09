from aiogram.enums import ContentType
from aiogram_dialog.api.entities import Context, MediaId, MediaAttachment


async def get_user_register_fields(
    aiogd_context: Context,
    **kwargs
) -> dict:
    dialog_data = aiogd_context.dialog_data

    dialog_data['photo'] = MediaAttachment(
        ContentType.PHOTO,
        file_id=MediaId(file_id=dialog_data.get('photo'))
    )
    dialog_data['languages'] = ', '.join(dialog_data.get('languages'))

    return dialog_data
