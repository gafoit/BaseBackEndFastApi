from typing import Optional, Literal

from pydantic import BaseModel, Field, EmailStr


class UserRegisterRequest(BaseModel):
    login: str
    password: str = Field(min_length=6)
    also_password: str = Field(min_length=6)
    email: EmailStr
    username: str


class UserLoginRequest(BaseModel):
    login: str
    password: str


class UserDeleteRequest(BaseModel):
    password: str


class UserUpdateRequest(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class RoleCreateRequest(BaseModel):
    name: str


class RoleDeleteRequest(BaseModel):
    name: str


class PermissionCreateRequest(BaseModel):
    object_type: Literal['file', 'role']
    action: Literal[
        'create',
        'give',  # Для раздачи ролей
        'read',
        'update',
        'delete',
        'read_all',
        'update_all',
        'delete_all'
    ]


class RolePermissionsCreateRequest(BaseModel):
    role_name: str
    object_type: Literal['file', 'role']
    action: Literal[
        'create',
        'give',  # Для раздачи ролей
        'read',
        'update',
        'delete',
        'read_all',
        'update_all',
        'delete_all'
    ]


class FileCreateRequest(BaseModel):
    user_id: int
    name: str
    content: str


class FileRequest(BaseModel):
    user_id: int
    name: str
