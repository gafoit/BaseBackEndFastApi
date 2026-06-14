import asyncio

from fastapi import FastAPI

from async_db import RolesService, PermissionsService, RolePermissionsService, \
    UserService
from src import *
from async_db.database_manager import manager
import logging_manager

from uvicorn import run


async def main():
    # Инициализация БД
    await manager.init_db()
    # Инициализация ролей в бд
    await RolesService(manager)._init_base_roles()
    await PermissionsService(manager)._init_permissions()
    await RolePermissionsService(manager)._init_base_roles_permissions()
    await UserService(manager).create_base_users()


# Очевидно БД должно инициализироваться до запуска приложения, иначе не хорошо
asyncio.run(main())
app = FastAPI()
app.include_router(AuthNRouter)
app.include_router(UserRouter)
app.include_router(RoleRouter)
app.include_router(PermissionRouter)
app.include_router(AdminRouter)
app.include_router(FileRouter)
run(app)
