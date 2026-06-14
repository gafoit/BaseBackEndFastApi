import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .BaseRepo import BaseRepo
from ..models import Users, RolePermissions

logger = logging.getLogger(__name__)


class UsersRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Users)

    async def create(self, login: str, role_id: int, password_hash: str,
                     email: str,
                     username: str,
                     is_active: bool, token_ver: int) -> Users:
        user = Users(
            login=login,
            role_id=role_id,
            password_hash=password_hash,
            email=email,
            username=username,
            is_active=is_active,
            token_ver=token_ver,
        )
        self._session.add(user)
        return user

    async def get_by_login(self, login: str) -> Users:
        return await self._session.scalar(select(Users).filter_by(login=login))

    async def get_by_email(self, email: str) -> Users:
        return await self._session.scalar(select(Users).filter_by(email=email))

    async def get_by_username(self, username: str) -> Users:
        return await self._session.scalar(
            select(Users).filter_by(username=username))

    async def get_permissions(self, user_id: int) -> RolePermissions:
        user = await self.get(user_id)
        await self._session.scalars(select(RolePermissions).filter_by(role_id=user.role_id))
