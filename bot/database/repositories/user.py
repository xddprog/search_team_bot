from sqlalchemy import select, and_

from database.models import UserModel
from database.repositories.base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = UserModel

    async def get_users_for_search_dialog(self, user_id: int, offset: int):
        this_user = await self.session.get(self.model, user_id)
        query = select(self.model).where(
            and_(
                self.model.id != user_id,
                self.model.id.notin_(this_user.watched_users),
                self.model.languages.any_()
            )
        ).limit(5).offset(offset)
        result = await self.session.execute(query)

        return result.scalars().all()