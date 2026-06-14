import logging
from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .BaseRepo import BaseRepo
from ..models import Files, Users

logger = logging.getLogger(__name__)


class FilesRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Files)

    async def create(self, user_id: int, name: str, content: str):
        obj = Files(user_id=user_id, name=name, content=content)
        self._session.add(obj)
        return obj

    async def get_by_user_name(self, user_id:int, name):
        res = await self._session.scalar(
            select(Files).filter_by(user_id=user_id, name=name))
        return res

    async def list_by_user(self, user_id):
        res = await self._session.scalars(select(Files).filter_by(user_id=user_id))
        return res.all()