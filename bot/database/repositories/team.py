from pydantic import UUID4
from sqlalchemy import select, not_
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.dialects.postgresql.operators import OVERLAP

from database.models import TeamModel, UserModel
from database.repositories.base import SqlAlchemyRepository


class TeamRepository(SqlAlchemyRepository):
    model = TeamModel

    async def delete_item(self, item_id: int | UUID4) -> list[UserModel]:
        team = await self.session.get(self.model, item_id)
        team_users = [user.id for user in team.users]
        team.users = []

        await self.session.delete(team)
        await self.session.commit()

        return team_users

    async def add_user_to_team(self, team_id: int, user: UserModel):
        team = await self.session.get(self.model, team_id)
        team.users.append(user)

        await self.session.commit()

    async def remove_user(self, team_id: int, user: UserModel):
        team = await self.session.get(self.model, team_id)
        team.users.remove(user)

        await self.session.commit()

    async def get_team_for_search_dialog(self, this_user: UserModel) -> TeamModel:
        query = select(self.model).filter(
            self.model.id.not_in(this_user.watched_teams),
            not_(self.model.users.any(UserModel.id == this_user.id)),
            OVERLAP(array(this_user.languages), self.model.languages)
        ).limit(1)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update_team_users(self, team_id: int, new_user: UserModel):
        team = await self.session.get(self.model, team_id)
        team_name = team.name

        team.users.append(new_user)

        await self.session.commit()
        return team_name
