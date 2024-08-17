from random import choice

from lorem import get_sentence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config.schemas import DatabaseConfig
from database.models import Base, UserModel
from utils.enums import Languages, SexTypes


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.engine = create_async_engine(
            url=f'postgresql+asyncpg://{config.db_user}:{config.db_pass}'
                f'@{config.db_host}:{config.db_port}/{config.db_name}',
            pool_size=100,
        )

    async def _create_users(self):
        session = await self.get_session()

        users_is_exists = await session.execute(select(UserModel))
        if users_is_exists.scalars().all():
            await session.close()
            return

        languages = [item.value for item in Languages]
        photos = [
            'AgACAgIAAxkBAAIPUWa82iFuwLuHNkKIIP4wGx8AAV-SgAACYuUxGyhK6Emr3VSF3ZVqsQEAAwIAA3MAAzUE',
            'AgACAgIAAxkBAAIPU2a82md-O9J6CYCrfWJut-v3Mm3gAAJj5TEbKEroSaVGUmLWV961AQADAgADcwADNQQ',
            'AgACAgIAAxkBAAIPVWa82m4LLNShODOhAAEJzUtZp7i3pwACZOUxGyhK6EkQYDT3CBkcHAEAAwIAA3MAAzUE',
            'AgACAgIAAxkBAAIPV2a82nVNJSWPgpqrJJK4sps04QuzAAJl5TEbKEroSanScTwyqh_TAQADAgADcwADNQQ',
            'AgACAgIAAxkBAAIPWWa82n149yOKUHir49MgHr_X8CDVAAJn5TEbKEroSdFjK9hJhX-7AQADAgADcwADNQQ',
            'AgACAgIAAxkBAAIPW2a82onUR4cuAWK6OJ0PToINBRyaAAJo5TEbKEroSfe7rD7z56-_AQADAgADcwADNQQ'
        ]

        for i in range(1, 100):
            user = UserModel(
                username=f'User_{i}',
                age=choice(range(12, 99)),
                sex=choice([SexTypes.FEMALE.value, SexTypes.MALE.value]),
                city=choice(['Москва', 'Санкт-Петербург', 'Нижний Новгород', 'Ижевск', 'Чайковский']),
                user_description=get_sentence(count=(1, 4)),
                languages=[choice(languages) for i in range(choice(range(1, 7)))],
                photo=choice(photos)
            )
            session.add(user)

        await session.commit()
        await session.close()

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await self._create_users()

    async def get_session(self) -> AsyncSession:
        return AsyncSession(self.engine)
