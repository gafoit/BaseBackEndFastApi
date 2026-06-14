from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from Models import *
from async_db import UserService, FilesService
from async_db.Exceptions import *
from async_db.database_manager import manager
from token_manager import JWTManager
from .dependencies import require_permission

router = APIRouter(prefix='/admin', tags=['Администрирование'])


@router.post('/roles/set')
async def set_role(user_login: str, role_name: str,
                   user_data=Depends(
                       require_permission('role', 'update'))):
    try:
        return await UserService(manager).change_role(user_login, role_name)
    except (RoleDoesNotExist, LoginDoesNotExist) as e:
        raise HTTPException(404, str(e))


@router.get('/files/read')
async def read_file(user_login: str, file_name: str, user_data=Depends(
    require_permission('file', 'read_all'))):
    try:
        user_id = await UserService(manager).get_id(user_login)
        return await FilesService(manager).read(
            FileRequest(user_id=user_id, name=file_name))
    except LoginDoesNotExist as e:
        raise HTTPException(404, str(e))


@router.get('/files/list_users')
async def list_files(user_login: str,
                     user_data=Depends(require_permission('file', 'read_all'))):
    try:
        user_id = await UserService(manager).get_id(user_login)
        return await FilesService(manager).list(user_id)
    except LoginDoesNotExist as e:
        raise HTTPException(404, str(e))


@router.post('/files/create')
async def create_file(user_login: str, file_name: str, content: str,
                      user_data=Depends(
                          require_permission('file', 'create_all'))):
    try:
        user_id = await UserService(manager).get_id(user_login)
        return await FilesService(manager).create(
            FileCreateRequest(user_id=user_id, name=file_name, content=content))
    except FileAlreadyExists as e:
        raise HTTPException(409, str(e))
    except LoginDoesNotExist as e:
        raise HTTPException(404, str(e))


@router.get('/files/delete')
async def delete_file(user_login: str, file_name: str,
                      user_data=Depends(
                          require_permission('file', 'delete_all'))):
    try:
        user_id = await UserService(manager).get_id(user_login)
        return await FilesService(manager).create(
            FileCreateRequest(user_id=user_id, name=file_name))
    except FileAlreadyExists as e:
        raise HTTPException(409, str(e))
    except LoginDoesNotExist as e:
        raise HTTPException(404, str(e))


@router.post('/files/update')
async def update_file(user_login: str, file_name: str, content: str,
                      user_data=Depends(
                          require_permission('file', 'update_all'))):
    try:
        user_id = await UserService(manager).get_id(user_login)
        return await FilesService(manager).create(
            FileCreateRequest(user_id=user_id, name=file_name, content=content))
    except FileAlreadyExists as e:
        raise HTTPException(409, str(e))
    except LoginDoesNotExist as e:
        raise HTTPException(404, str(e))
