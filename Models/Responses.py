from pydantic import BaseModel


class RegisterResponse(BaseModel):
    status: str
    login: str


class LoginResponse(BaseModel):
    status: str
    refresh_token: str


class LogoutResponse(BaseModel):
    status: str
    msg: str


class DeleteResponse(BaseModel):
    status: str
    msg: str


class UserUpdateResponse(BaseModel):
    status: str
    field_update: dict[str, bool]


class CreateRoleResponse(BaseModel):
    status: str
    name: str


class DeleteRoleResponse(BaseModel):
    status: str
    name: str


class PermissionCreateResponse(BaseModel):
    status: str
    # Ключ - объект, значение действие с ним
    obj: dict[str, str]
