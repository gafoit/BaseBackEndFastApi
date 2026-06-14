from fastapi import APIRouter, Depends, HTTPException

from Models import UserSchema, LogoutResponse, UserDeleteRequest, DeleteResponse, \
    UserUpdateResponse, UserUpdateRequest, VisibleUserData
from async_db import UserService
from async_db.Exceptions import *
from async_db.database_manager import manager
from src.Users.dependencies import get_current_user

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.post('/logout', response_model=LogoutResponse,
             summary='Выход пользователя')
async def logout(user_data: UserSchema = Depends(get_current_user)):
    try:
        res = await UserService(manager).logout(user_data.id)
    except UserDoesNotExist as e:
        raise HTTPException(400, detail=str(e))
    else:
        return LogoutResponse(**res)


@router.post('/delete', response_model=DeleteResponse,
             summary='Удаление пользователя')
async def delete_user(request: UserDeleteRequest,
                      user_data: UserSchema = Depends(get_current_user)):
    try:
        res = await UserService(manager).delete(user_data.id, request.password)
    except UserDoesNotExist as e:
        raise HTTPException(400, detail=str(e))
    except InvalidPassword as e:
        raise HTTPException(403, detail=str(e))
    else:
        return DeleteResponse(**res)


@router.patch('/update', response_model=UserUpdateResponse,
              summary='Обновление информации пользователя')
async def update(new_data: UserUpdateRequest,
                 user_data: UserSchema = Depends(get_current_user)):
    try:
        res = await UserService(manager).update_user(user_data.id, new_data)
    except UserDoesNotExist as e:
        raise HTTPException(400, detail=str(e))
    except (RepeatsOldPassword, LoginAlreadyExists, EmailAlreadyExists,
            UsernameAlreadyExists) as e:
        raise HTTPException(409, detail=str(e))
    else:
        return res


@router.get('/me')
async def me(
        user_data: UserSchema = Depends(get_current_user)) -> VisibleUserData:
    return VisibleUserData(
        login=user_data.login,
        email=user_data.email,
        username=user_data.username
    )
