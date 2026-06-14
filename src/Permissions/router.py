from typing import List

from fastapi import APIRouter, Depends, HTTPException

from Models import PermissionCreateResponse, PermissionCreateRequest, \
    PermissionsSchema, UserSchema
from async_db.Exceptions import *
from async_db import PermissionsService
from async_db.database_manager import manager
from .dependencies import require_permission

router = APIRouter(prefix='/perms', tags=['Разрешения'])


@router.post('/add')
async def add_permission(request: PermissionCreateRequest,
                         user_data: UserSchema = Depends(
                             require_permission('role', 'update'))):
    try:
        return await PermissionsService(manager).create(request)
    except ObjectActionAlreadyExists as e:
        raise HTTPException(409, str(e))


@router.get("/list")
async def list_permissions(
        user_data: UserSchema = Depends(
            require_permission('role', 'update'))):
    return await PermissionsService(manager).list()


@router.get('/list_by_obj')
async def list_by_obj(obj_type: str, user_data: UserSchema = Depends(
    require_permission('role', 'delete'))):
    return await PermissionsService(manager).list_by_obj(obj_type)
