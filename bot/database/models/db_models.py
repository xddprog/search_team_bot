from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import BigInteger, String, ARRAY, Enum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.models import Base
from utils.enums import SexTypes


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    sex: Mapped[str]
    age: Mapped[int] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    languages: Mapped[list] = mapped_column(ARRAY(String), nullable=False)
    user_description: Mapped[str] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column(nullable=False)
    watched_users = mapped_column(ARRAY(BigInteger), default=[])
    watched_teams = mapped_column(ARRAY(BigInteger), default=[])

    teams: Mapped[list['TeamModel']] = relationship(
        back_populates='users',
        secondary='user_teams',
        uselist=True,
        lazy='selectin'
    )

    async def to_dict(self):
        user = {key: value for key, value in self.__dict__.items()}
        user['languages'] = ', '.join(user['languages'])
        user['photo'] = MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(file_id=user['photo'])
        )

        return user


class TeamModel(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    team_description: Mapped[str]
    photo: Mapped[str]
    languages = mapped_column(ARRAY(String), nullable=False)
    admins = mapped_column(ARRAY(BigInteger), nullable=False)

    users: Mapped[list['UserModel']] = relationship(
        back_populates='teams',
        secondary='user_teams',
        uselist=True,
        lazy='joined'
    )

    async def to_dict(self):
        team = {key: value for key, value in self.__dict__.items()}
        team['languages'] = ', '.join(team['languages'])
        team['photo'] = MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(file_id=team['photo'])
        )
        team['users'] = [(user.id, user.username) for user in team['users']]
        return team


class UserTeamsModel(Base):
    __tablename__ = 'user_teams'
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    team_fk: Mapped[int] = mapped_column(ForeignKey('teams.id'), primary_key=True)
