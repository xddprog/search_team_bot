import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs

import dialogs
from config.loads import get_bot_config, get_database_config
from database.connection.pg_connection import DatabaseConnection
from middlewares.db_middleware import DatabaseMiddleware


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    bot_config = get_bot_config()
    db_config = get_database_config()

    bot = Bot(token=bot_config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    db_connection = DatabaseConnection(config=db_config)

    await db_connection.create_tables()

    dp.include_routers(
        dialogs.dialogs_router,
        dialogs.register_dialog,
        dialogs.menu_dialog,
        dialogs.main_profile_dialog,
        dialogs.edit_profile_dialog,
        dialogs.delete_profile_dialog,
        dialogs.user_teams_dialog,
        dialogs.create_team_dialog,
        dialogs.view_team_dialog,
        dialogs.accept_invite_to_team_dialog,
        dialogs.delete_team_dialog,
        dialogs.view_team_user_dialog,
        dialogs.remove_team_user_dialog
    )

    dp.update.middleware(DatabaseMiddleware(db_connection=db_connection))

    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())