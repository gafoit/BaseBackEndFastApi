from fastapi import APIRouter, HTTPException

from Models import UserRegisterRequest, RegisterResponse, UserLoginRequest, \
    LoginResponse
from async_db import UserService
from async_db.Exceptions import *
from async_db.database_manager import manager
from token_manager import JWTManager

router = APIRouter(prefix='/authentication', tags=['Аутентификация'])


@router.post('/register', response_model=RegisterResponse,
             summary='Регистрация пользователя')
async def register(request: UserRegisterRequest):
    try:
        reg_resp = await UserService(manager).register_user(request, 'user')
    except (LoginAlreadyExists, EmailAlreadyExists, UnmatchedPassword) as e:
        raise HTTPException(409, detail=str(e))
    else:
        return reg_resp


@router.post('/login', response_model=LoginResponse,
             summary='Вход пользователя')
async def login(request: UserLoginRequest):
    try:
        user_data = await UserService(manager).login(request)
    except UserDoesNotExist as e:
        raise HTTPException(400, detail=str(e))
    except (UserBlocked, InvalidPassword) as e:
        raise HTTPException(403, detail=str(e))
    else:
        token = JWTManager.create_token(user_data.id, user_data.token_ver)
        return LoginResponse(status='success', refresh_token=token)
