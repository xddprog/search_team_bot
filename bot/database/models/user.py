from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import BigInteger, String, ARRAY, Enum
from sqlalchemy.orm import mapped_column, Mapped

from database.models import Base
from utils.enums import SexTypes


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    sex: Mapped[str]
    age: Mapped[int] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    languages = mapped_column(ARRAY(String), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column(nullable=False)
    watched_users = mapped_column(ARRAY(String), nullable=True)

    async def to_dict(self):
        user = {key: value for key, value in self.__dict__.items()}
        user['languages'] = ', '.join(user['languages'])
        user['photo'] = MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(file_id=user['photo'])
        )
        return user
