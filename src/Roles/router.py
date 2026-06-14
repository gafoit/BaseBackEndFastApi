from typing import List

from fastapi import APIRouter, Depends, HTTPException

from Models import RoleCreateRequest, CreateRoleResponse, DeleteRoleResponse, \
    RoleDeleteRequest, RoleSchema, UserSchema, RolePermissionsCreateRequest, \
    RolePermissionsSchema
from async_db.Exceptions import *
from async_db import RolesService, RolePermissionsService
from async_db.database_manager import manager
from .dependencies import require_permission,get_current_user

router = APIRouter(prefix='/roles', tags=['Роли'])


@router.post('/add', response_model=CreateRoleResponse)
async def create_role(request: RoleCreateRequest,
                      user_data: UserSchema = Depends(
                          require_permission('role', 'create'))):
    try:
        return await RolesService(manager).create_role(request)
    except RoleAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post('/delete', response_model=DeleteRoleResponse)
async def delete_role(request: RoleDeleteRequest,
                      user_data: UserSchema = Depends(
                          require_permission('role', 'delete'))):
    try:
        return await RolesService(manager).delete_role(request)
    except RoleDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/list", response_model=List[RoleSchema])
async def list_roles(user_data: UserSchema = Depends(
    require_permission('role', 'read_all'))):
    return await RolesService(manager).list_roles()


@router.post('/add_permission')
async def add_permission(request: RolePermissionsCreateRequest,
                         user_data=Depends(
                             require_permission('role', 'update'))):
    try:
        new_id = await RolePermissionsService(manager).create(request)
    except RoleDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {'status': 'success', 'id': new_id}


@router.post('/remove_permission')
async def remove_permission(request: RolePermissionsCreateRequest,
                            user_data=Depends(
                                require_permission('role', 'update'))):
    try:
        res = await RolePermissionsService(manager).create(request)
    except RoleDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))
    return res


@router.get('/permissions')
async def get_permissions(role_name: str, user_data=Depends(
    require_permission('role', 'read_all'))):
    try:
        return await RolePermissionsService(manager).get_role_perms(
            role_name)
    except RoleDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/get', response_model=RoleSchema)
async def get_role(user_data=Depends(get_current_user)):
    try:
        return await RolesService(manager).get_role(user_data.role_id)
    except RoleDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))
