from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.dialects.postgresql.operators import OVERLAP

from database.models import UserModel
from database.repositories.base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = UserModel

    async def get_users_for_search_dialog(self, user_id: int, offset: int) -> list[UserModel]:
        this_user: UserModel = await self.session.get(self.model, user_id)

        query = select(self.model).filter(
            self.model.id != user_id,
            self.model.id.not_in(this_user.watched_users),
            OVERLAP(array(this_user.languages), self.model.languages)
        ).limit(5).offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_user_watched_users(self, user_id: int, new_watched_user: int) -> dict:
        user: UserModel = await self.session.get(self.model, user_id)
        user.watched_users = [*user.watched_users, new_watched_user]

        await self.session.commit()
        await self.session.refresh(user)

        return await user.to_dict()
