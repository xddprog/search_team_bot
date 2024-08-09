from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config.schemas import DatabaseConfig
from database.models import Base


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.engine = create_async_engine(
            url=f'postgresql+asyncpg://{config.db_user}:{config.db_pass}'
                f'@{config.db_host}:{config.db_port}/{config.db_name}'
        )

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        return AsyncSession(self.engine)
