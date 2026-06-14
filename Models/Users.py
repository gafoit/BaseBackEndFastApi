from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    role_id: int
    login: str
    email: str
    username: str

    is_active: bool
    token_ver: int


class VisibleUserData(BaseModel):
    login: str
    email: str
    username: str


class PublicUserData(BaseModel):
    username: str
