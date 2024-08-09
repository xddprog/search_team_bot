from pprint import pprint
from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection.pg_connection import DatabaseConnection
from database.db_main import Database


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        session = await self.db_connection.get_session()
        try:
            data['database'] = Database(session=session)
            return await handler(event, data)
        finally:
            await session.close()
