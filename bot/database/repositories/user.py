from database.models import UserModel
from database.repositories.base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = UserModel