from typing import List

from ..database_manager import DBManager
from ..Repos import PermissionsRepo
from ..Exceptions import *
from Models import PermissionCreateRequest, PermissionCreateResponse, \
    PermissionsSchema
from .BaseService import BaseService


class PermissionsService(BaseService):

    async def _init_permissions(self):
        obj_types = ['file', 'role']
        actions = [
            {'create', 'create_all', 'read', 'update', 'delete', 'read_all',
             'update_all',
             'delete_all'},
            {'create', 'give', 'read', 'update', 'delete', 'read_all',
             'update_all', 'delete_all'}
        ]
        async with self._db.session() as s:
            permissions_repo = PermissionsRepo(s)
            existing_actions = [await permissions_repo.list_object_actions(obj)
                                for obj
                                in obj_types]
            # Создаём словари ключ - тип объект, значение - ключи которые
            # Необходимо создать
            to_create = [
                PermissionsSchema(object_type=obj_types[i],
                                  actions=actions[i]) if len(
                    existing_actions[i]) == 0 else PermissionsSchema(
                    object_type=obj_types[i], actions=actions[
                        i].difference(existing_actions[i])) for i in
                range(len(obj_types))]
            for params in to_create:
                await permissions_repo.bulk_create(**params.model_dump())

    async def create(self, request: PermissionCreateRequest):
        async with self._db.session() as s:
            permissions = PermissionsRepo(s)
            existing_actions = await permissions.list_object_actions(
                request.object_type)
            # Если для объекта уже есть такое разрешение, то снова не создаём
            if request.action in existing_actions:
                raise ObjectActionAlreadyExists(**request.model_dump())

            obj = await permissions.create(**request.model_dump())
            return PermissionCreateResponse(status='success',
                                            obj={obj.object_type: obj.action})

    async def list(self) -> List[PermissionsSchema]:
        async with self._db.session() as s:
            permissions_repo = PermissionsRepo(s)
            res = [
                PermissionsSchema(object_type=obj_type,
                                  actions=await \
                                      permissions_repo.list_object_actions(
                                          obj_type)) for obj_type in
                await permissions_repo.list_object_types()]
            return res

    async def list_by_obj(self, obj_type: str) -> PermissionsSchema:
        async with self._db.session() as s:
            permissions_repo = PermissionsRepo(s)
            return await permissions_repo.list_object_actions(obj_type)

    async def check_permissions(self, user_id: int, obj_type: str,
                                action: str) -> bool:
        async with self._db.session() as s:
            permissions_repo = PermissionsRepo(s)
            return await permissions_repo.check_permissions(user_id, obj_type,
                                                            action)
