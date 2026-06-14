from typing import List

from ..database_manager import DBManager
from ..Repos import PermissionsRepo, RolesRepo, RolePermissionsRepo
from ..Exceptions import *
from Models import PermissionCreateRequest, PermissionCreateResponse, \
    PermissionsSchema, RolePermissionsSchema, RolePermissionsCreateRequest
from .BaseService import BaseService


class RolePermissionsService(BaseService):
    async def _init_base_roles_permissions(self):
        base_roles = ['admin', 'helper', 'user']
        base_objects = ['file', 'role']
        async with self._db.session() as s:

            roles_repo = RolesRepo(s)
            base_roles_dict = {role.name: role.id for role in
                               await roles_repo.list_by_names(base_roles)}
            permissions_repo = PermissionsRepo(s)
            role_permissions_repo = RolePermissionsRepo(s)
            # Словарь - ключи объект, значения - (действие, id)
            # print(await permissions_repo.dict_permissions())
            all_perms = {
                obj_name: [(perm.action, perm.id) for perm in
                           await permissions_repo.list_permissions(obj_name)]
                for obj_name in base_objects
            }
            to_create = []
            # cursed programming №1
            for role_name, role_id in base_roles_dict.items():
                if role_name == 'admin':
                    perms_id = {action[1] for obj_name, perm in
                                all_perms.items()
                                for action in perm}
                elif role_name == 'helper':
                    perms_id = {action[1] for obj_name, perm in
                                all_perms.items() for action in perm
                                if obj_name == 'file' and
                                ('all' not in action[0]
                                 or action[0] == 'read_all')}
                elif role_name == 'user':
                    perms_id = {action[1] for obj_name, perm in
                                all_perms.items() for action in perm if
                                obj_name == 'file' and not 'all' in action[0]}
                else:
                    continue
                existing_perms_for_role = set([perm.id for perm in
                                               await role_permissions_repo.get_role_perms(
                                                   role_id)])
                if len(existing_perms_for_role) > 0:
                    perms_id.difference_update(
                        existing_perms_for_role)
                if len(perms_id) > 0:
                    to_create.append(RolePermissionsSchema(role_id=role_id,
                                                           permission_ids=perms_id))
            if len(to_create) > 0:
                for schema in to_create:
                    print(schema)
                    await role_permissions_repo.bulk_create(
                        **schema.model_dump())
            await s.flush()

    async def get_role_permissions(self, role_name: str):
        async with self._db.session() as s:
            roles_repo = RolesRepo(s)
            role = await roles_repo.get_by_name(role_name)
            if role is None:
                raise RoleDoesNotExist(role_name)
            role_permissions_repo = RolePermissionsRepo(s)
            res = await role_permissions_repo.get_role_perms(role.id)
            return {
                obj: [perm.action for perm in res]
                for obj in {obj.object_type for obj in res}
            }

    async def get_role_perms(self, role_name: str):
        async with self._db.session() as s:
            roles_repo = RolesRepo(s)
            role = await roles_repo.get_by_name(role_name)
            if role is None:
                raise RoleDoesNotExist(role_name)
            role_permissions_repo = RolePermissionsRepo(s)

            return await role_permissions_repo.role_perms_dict(role.id)

    async def create(self, request: RolePermissionsCreateRequest):
        async with self._db.session() as s:
            roles_repo = RolesRepo(s)
            role = await roles_repo.get_by_name(request.role_name)
            if role is None:
                raise RoleDoesNotExist(request.role_name)
            permissions_repo = PermissionsRepo(s)
            perm = await permissions_repo.get_by_obj_action(request.object_type,
                                                            request.action)
            role_permissions_repo = RolePermissionsRepo(s)
            rp = await role_permissions_repo.create(role.id, perm.id)
            await s.flush()
            return rp.id

    async def delete(self, request: RolePermissionsCreateRequest):
        async with self._db.session() as s:
            roles_repo = RolesRepo(s)
            role = await roles_repo.get_by_name(request.role_name)
            if role is None:
                raise RoleDoesNotExist(request.role_name)
            permissions_repo = PermissionsRepo(s)
            perm = await permissions_repo.get_by_obj_action(request.object_type,
                                                            request.action)
            role_permissions_repo = RolePermissionsRepo(s)
            rp = role_permissions_repo.get_by_ids(role.id, perm.id)
            if rp is None:
                return {'status': 'already deleted'}
            await role_permissions_repo.delete(rp)
            await s.flush()
            return {'status': 'deleted'}
