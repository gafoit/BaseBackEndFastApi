from fastapi import APIRouter, Depends, HTTPException

from Models import FileCreateRequest, FileRequest
from async_db import UserService, FilesService
from async_db.Exceptions import *
from async_db.database_manager import manager
from src.Users.dependencies import get_current_user

router = APIRouter(prefix='/files', tags=['Файлы'])


@router.post('/create')
async def create_file(name: str, content: str,
                      user_data=Depends(get_current_user)):
    try:
        return await FilesService(manager).create(
            FileCreateRequest(name=name, content=content, user_id=user_data.id))
    except UserDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))
    except FileAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get('/read')
async def get_file(name: str, user_data=Depends(get_current_user)):
    try:
        return await FilesService(manager).read(
            FileRequest(name=name, user_id=user_data.id))
    except (UserDoesNotExist, FileNotFound) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/update')
async def update_file(name: str, content: str,
                      user_data=Depends(get_current_user)):
    try:
        return await FilesService(manager).update(
            FileCreateRequest(name=name, content=content, user_id=user_data.id))
    except (UserDoesNotExist, FileNotFound) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/delete')
async def delete_file(name: str, user_data=Depends(get_current_user)):
    try:
        return await FilesService(manager).delete(
            FileRequest(name=name, user_id=user_data.id))
    except UserDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/list')
async def list(user_data=Depends(get_current_user)):
    return await FilesService(manager).list(user_data.id)
