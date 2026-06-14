import logging
from typing import Generic, TypeVar, Type, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
logger = logging.getLogger(__name__)


class BaseRepo(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self._session = session
        self._model = model

    async def get(self, id: int) -> T | None:
        return await self._session.get(self._model, id)

    async def list(self) -> List[T]:
        stmt = select(self._model)
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def list_by_ids(self, ids: List[int]) -> List[T]:
        stmt = select(self._model).where(self._model.id.in_(ids))
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def delete(self, obj: T) -> None:
        await self._session.delete(obj)

    async def delete_by_id(self, id: int) -> None:
        obj = await self.get(id)
        if obj:
            await self._session.delete(obj)

    async def clear(self) -> None:
        for obj in await self.list():
            await self._session.delete(obj)
