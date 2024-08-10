from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.team import TeamRepository
from database.repositories.user import UserRepository


class Database:
    def __init__(self, session: AsyncSession) -> None:
        self.users: UserRepository = UserRepository(session=session)
        self.teams: TeamRepository = TeamRepository(session=session)
