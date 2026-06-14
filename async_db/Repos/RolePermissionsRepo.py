import logging
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .BaseRepo import BaseRepo
from ..models import RolePermissions, Permissions, Roles

logger = logging.getLogger(__name__)


class RolePermissionsRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RolePermissions)

    async def create(self, role_id: int, perm_id: int) -> RolePermissions:
        obj = RolePermissions(role_id=role_id, permission_id=perm_id)
        self._session.add(obj)
        return obj

    async def bulk_create(self, role_id: int,
                          permission_ids: List[int]) -> List[RolePermissions]:
        objs = [RolePermissions(role_id=role_id, permission_id=perm_id) for
                perm_id in
                permission_ids]
        self._session.add_all(objs)
        return objs

    async def get_role_perms(self, role_id: int) -> List[Permissions]:
        res = await self._session.scalars(
            select(Permissions)
            .join(RolePermissions).filter_by(role_id=role_id)
        )

        return list(res.all())

    async def role_perms_dict(self, role_id: int) -> dict:
        res = await self._session.scalars(
            select(Permissions)
            .join(RolePermissions).filter_by(role_id=role_id)
        )
        res = res.all()
        return {
            obj: [perm.action for perm in res if perm.object_type == obj]
            for obj in {obj.object_type for obj in res}
        }

    async def get_permission_roles(self, perm_id: int) -> List[Roles]:
        res = await self._session.scalars(
            select(RolePermissions).filter_by(permission_id=perm_id))
        return [rp.role for rp in res.all()]

    async def get_by_ids(self, role_id: int, perm_id: int) -> RolePermissions:
        res = await self._session.scalar(
            select(RolePermissions).filter_by(role_id=role_id,
                                              permission_id=perm_id)
        )
        return res
