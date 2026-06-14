import logging
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .BaseRepo import BaseRepo
from ..models import Roles, RolePermissions

logger = logging.getLogger(__name__)


class RolesRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Roles)

    async def create(self, name: str) -> Roles:
        role = Roles(name=name)
        self._session.add(role)
        return role

    async def bulk_create(self, names: List[str]) -> List[Roles]:
        roles = [Roles(name=name) for name in names]
        self._session.add_all(roles)
        return roles

    async def get_by_name(self, name: str) -> Roles:
        return await self._session.scalar(select(Roles).filter_by(name=name))

    async def list_by_names(self, names: List[str]) -> List[Roles]:
        res = await self._session.scalars(
            select(Roles).filter(Roles.name.in_(names)))
        return list(res.all())
