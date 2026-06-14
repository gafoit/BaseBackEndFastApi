import asyncio

from pydantic import BaseModel

from password_manager import PasswordManager
from ..Repos import UsersRepo, RolesRepo, RolePermissionsRepo
from ..Exceptions import *
from Models import UserRegisterRequest, RegisterResponse, UserLoginRequest, \
    UserSchema, \
    UserUpdateRequest, UserUpdateResponse
from .BaseService import BaseService


class UserService(BaseService):
    async def create_base_users(self):
        users_names = {'Admin', 'Helper', 'User'}
        async with self._db.session() as s:
            users_repo = UsersRepo(s)
            roles_repo = RolesRepo(s)
            for user_name in users_names:
                role = await roles_repo.get_by_name(user_name.lower())
                if role is None:
                    raise RoleDoesNotExist(user_name.lower())
                login_check = await users_repo.get_by_login(user_name)
                if login_check is not None:
                    continue
                await users_repo.create(
                    user_name,
                    role.id,
                    await asyncio.to_thread(
                        PasswordManager.hash_password, user_name
                    ),
                    f"{user_name}_fake_email@example.com",
                    user_name,
                    True,
                    1
                )

    async def register_user(self, register_request: UserRegisterRequest,
                            role_name: str):
        async with self._db.session() as s:
            if register_request.password != register_request.also_password:
                raise UnmatchedPassword()
            users_repo = UsersRepo(s)
            roles_repo = RolesRepo(s)

            role = await roles_repo.get_by_name(role_name)
            if role is None:
                raise RoleDoesNotExist(role_name)

            login_taken = await users_repo.get_by_login(
                register_request.login) is not None
            email_registered = await users_repo.get_by_email(
                register_request.email) is not None
            if login_taken:
                raise LoginAlreadyExists(register_request.login)
            if email_registered:
                raise EmailAlreadyExists(register_request.email)

            user = await users_repo.create(
                register_request.login,
                role.id,
                await asyncio.to_thread(
                    PasswordManager.hash_password, register_request.password
                ),
                register_request.email,
                register_request.username,
                True,
                1

            )
            await s.flush()
            return RegisterResponse(status='success', login=user.login)

    async def login(self, login_request: UserLoginRequest) -> UserSchema:
        async with self._db.session() as s:
            users_repo = UsersRepo(s)
            user = await users_repo.get_by_login(login_request.login)
            if user is None:
                raise LoginDoesNotExist(login_request.login)
            if not user.is_active:
                raise UserBlocked()
            # Сверка паролей
            password_check = await asyncio.to_thread(
                PasswordManager.verify_password,
                login_request.password, user.password_hash
            )
            if not password_check:
                raise InvalidPassword()
            return UserSchema(
                id=user.id,
                role_id=user.role_id,
                login=user.login,
                email=user.email,
                username=user.username,
                is_active=user.is_active,
                token_ver=user.token_ver
            )

    async def check_user(self, user_id: int, token_ver: int):
        async with self._db.session() as s:
            users_repo = UsersRepo(s)
            user = await users_repo.get(user_id)
            if user is None:
                raise UserDoesNotExist()
            if user.token_ver != token_ver:
                raise UserLoggedOut()
            if not user.is_active:
                raise UserBlocked()
            return UserSchema(
                id=user.id,
                role_id=user.role_id,
                login=user.login,
                email=user.email,
                username=user.username,
                is_active=user.is_active,
                token_ver=user.token_ver
            )

    async def logout(self, user_id: int):
        async with self._db.session() as s:
            users_repo = UsersRepo(s)
            user = await users_repo.get(user_id)
            if user is None:
                raise UserDoesNotExist()
            user.token_ver += 1
            await s.flush()
            return {'status': 'success', 'msg': 'Logged Out'}

    async def delete(self, user_id: int, password: str):
        async with self._db.session() as s:
            users_repo = UsersRepo(s)
            user = await users_repo.get(user_id)
            if user is None:
                raise UserDoesNotExist()
            # Сверка паролей
            password_check = await asyncio.to_thread(
                PasswordManager.verify_password,
                password, user.password_hash
            )
            if not password_check:
                raise InvalidPassword()
            user.is_active = False
            await s.flush()
            return {'status': 'success', 'msg': 'User deleted'}

    async def update_user(self, user_id: int,
                          data: UserUpdateRequest) -> UserUpdateResponse:
        async with self._db.session() as s:
            to_update = data.model_dump(exclude_unset=True)
            users_repo = UsersRepo(s)
            user = await users_repo.get(user_id)
            if user is None:
                raise UserDoesNotExist()
            updated_fields = {}
            if 'login' in to_update:
                unique_check = await users_repo.get_by_login(to_update['login'])
                if unique_check and unique_check.id != user.id:
                    raise LoginAlreadyExists(to_update['login'])
            if 'email' in to_update:
                unique_check = await users_repo.get_by_email(to_update['email'])
                if unique_check and unique_check.id != user.id:
                    raise EmailAlreadyExists(to_update['email'])

            if 'username' in to_update:
                unique_check = await users_repo.get_by_username(
                    to_update['username'])
                if unique_check and unique_check.id != user.id:
                    raise UsernameAlreadyExists(to_update['username'])

            if 'password' in to_update:
                password_check = await asyncio.to_thread(
                    PasswordManager.verify_password,
                    to_update['password'], user.password_hash
                )
                if password_check:
                    raise RepeatsOldPassword()
                else:
                    user.password_hash = await asyncio.to_thread(
                        PasswordManager.hash_password, to_update.pop('password')
                    )
                    # При обновлении пароля делаем перезаход
                    user.token_ver += 1
                    updated_fields['password'] = True
            for field, value in to_update.items():
                setattr(user, field, value)
                updated_fields[field] = True
            await s.flush()
            return UserUpdateResponse(status='success',
                                      field_update=updated_fields)

    async def change_role(self, login: str, role_name: str):
        async with self._db.session() as s:
            users_repo = UsersRepo(s)
            roles_repo = RolesRepo(s)
            user = await users_repo.get_by_login(login)
            if user is None:
                raise UserDoesNotExist()
            role = await roles_repo.get_by_name(role_name)
            if role is None:
                raise RoleDoesNotExist(role_name)
            user.role_id = role.id
            await s.flush()
            return {'status': 'success', 'msg': f'Role changed to {role_name}'}

    async def get_id(self, login: str):
        async with self._db.session() as s:
            users_repo = UsersRepo(s)
            user = await users_repo.get_by_login(login)
            if user is None:
                raise LoginDoesNotExist(login)
            return user.id
