import logging
from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .BaseRepo import BaseRepo
from ..models import Permissions, RolePermissions, Roles, Users

logger = logging.getLogger(__name__)


class PermissionsRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Permissions)

    async def create(self, obj_type: str, action: str):
        obj = Permissions(object_type=obj_type, action=action)
        self._session.add(obj)
        return obj

    async def bulk_create(self, object_type: str, actions: List[str]):
        objs = [Permissions(object_type=object_type, action=action) for action
                in
                actions]
        self._session.add_all(objs)
        return objs

    async def list_object_actions(self, obj_type: str):
        res = await self._session.scalars(
            select(Permissions).filter_by(object_type=obj_type))
        return [r.action for r in res.all()]

    async def list_object_types(self):
        res = await self._session.scalars(select(Permissions.object_type))
        return res.unique().all()

    async def list_permissions(self, obj_type: str):
        res = await self._session.scalars(
            select(Permissions).filter_by(object_type=obj_type))
        return res.all()

    async def check_permissions(self, user_id: int, obj_type: str, action: str):
        res = await self._session.scalar(
            select(Permissions)
            .join(RolePermissions)
            .join(Roles)
            .join(Users)
            .where(
                and_(
                    Users.id == user_id,
                    Permissions.object_type == obj_type,
                    Permissions.action == action
                )
            )
        )
        return res is not None

    async def get_by_obj_action(self, obj_type: str, action: str):
        res = await self._session.scalar(
            select(Permissions).filter_by(object_type=obj_type, action=action)
        )
        return res