from database.models import TeamModel, UserModel
from database.repositories.base import SqlAlchemyRepository


class TeamRepository(SqlAlchemyRepository):
    model = TeamModel

    async def add_user_to_team(self, team_id: int, user: UserModel):
        team = await self.session.get(TeamModel, team_id)
        team.users.append(user)

        await self.session.commit()