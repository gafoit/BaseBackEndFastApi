from ..database_manager import DBManager
from ..Repos import RolesRepo
from ..Exceptions import *
from Models import RoleCreateRequest, CreateRoleResponse, DeleteRoleResponse, \
    RoleDeleteRequest, RoleSchema
from .BaseService import BaseService


class RolesService(BaseService):
    async def _init_base_roles(self):
        base_roles = {'admin', 'helper', 'user'}
        async with self._db.session() as s:
            roles = RolesRepo(s)
            existing = [role.name for role in await roles.list()]

            if not len(existing):
                to_create = base_roles.copy()
            else:
                to_create = base_roles.difference(set(existing))
            if len(to_create):
                await roles.bulk_create(list(to_create))

    async def create_role(self,
                          request: RoleCreateRequest) -> CreateRoleResponse:
        async with self._db.session() as s:
            roles = RolesRepo(s)
            if await roles.get_by_name(request.name) is not None:
                raise RoleAlreadyExists(request.name)
            role = await roles.create(request.name)
            await s.flush()
            return CreateRoleResponse(status='success', name=role.name)

    async def delete_role(self,
                          request: RoleDeleteRequest) -> DeleteRoleResponse:
        async with self._db.session() as s:
            roles = RolesRepo(s)
            role = await roles.get_by_name(request.name)
            if role is None:
                raise RoleDoesNotExist(request.name)
            await roles.delete(role)
            return DeleteRoleResponse(status='success', name=role.name)

    async def list_roles(self):
        async with self._db.session() as s:
            roles = RolesRepo(s)
            return [RoleSchema(name=r.name) for r in await roles.list()]

    async def get_role(self, role_id: int):
        async with self._db.session() as s:
            roles = RolesRepo(s)
            role = await roles.get(role_id)
            if role is None:
                raise RoleDoesNotExist(str(role_id))
            return RoleSchema(name=role.name)
