from abc import ABC, abstractmethod
from typing import Type

from pydantic import UUID4
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserModel


SqlalchemyModel = Type[UserModel]


class BaseRepository(ABC):
    @abstractmethod
    async def get_item(self, item_id: int | UUID4):
        raise NotImplementedError

    @abstractmethod
    async def get_all_items(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_attribute(self, attribute, value: str | UUID4 | int):
        raise NotImplementedError

    @abstractmethod
    async def add_item(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_item(self, item_id: int | UUID4):
        raise NotImplementedError

    @abstractmethod
    async def update_item(self, item_id: int | UUID4, kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(BaseRepository):
    model: SqlalchemyModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_item(self, item_id: int | UUID4) -> SqlalchemyModel:
        item = await self.session.get(self.model, item_id)

        return item

    async def get_all_items(self) -> SqlalchemyModel:
        query = select(self.model)
        items = await self.session.execute(query)

        return items.scalars().all()

    async def get_by_attribute(self, attribute, value: str | UUID4 | int) -> SqlalchemyModel:
        query = select(self.model).where(attribute == value)
        items = await self.session.execute(query)

        return items.scalars().all()

    async def add_item(self, **kwargs) -> SqlalchemyModel:
        item = self.model(**kwargs)

        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)

        return item

    async def delete_item(self, item_id: int | UUID4):
        deleting_item = await self.session.get(self.model, item_id)
        await self.session.delete(deleting_item)
        await self.session.commit()

    async def update_item(self, item_id: int, update_values: dict):
        query = update(self.model).where(self.model.id == item_id).values(update_values)
        await self.session.execute(query)
        await self.session.commit()
