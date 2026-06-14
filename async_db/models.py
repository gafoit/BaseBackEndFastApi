from typing import List

from sqlalchemy import ForeignKey, LargeBinary, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    users: Mapped[list["Users"]] = relationship('Users', back_populates="role")
    role_permissions: Mapped[List["RolePermissions"]] = relationship(
        'RolePermissions', back_populates="role",
        cascade="all, delete-orphan"
        # Если удалим роль, то удалится и связь роли с правом
    )


class Permissions(Base):
    __tablename__ = "permissions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    object_type: Mapped[str]
    action: Mapped[str]

    role_permissions: Mapped[List["RolePermissions"]] = relationship(
        'RolePermissions',
        back_populates="permission")


class RolePermissions(Base):
    __tablename__ = "role_permissions"
    __table_args__ = (
        # Чтобы не повторить для одной роли то же право
        UniqueConstraint(
            "role_id",
            "permission_id",
            name="uq_role_permission"
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"),
                                               nullable=False)
    role: Mapped["Roles"] = relationship(back_populates="role_permissions")
    permission: Mapped["Permissions"] = relationship(
        back_populates="role_permissions")


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False)

    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    token_ver: Mapped[int] = mapped_column(nullable=False)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)

    role: Mapped["Roles"] = relationship(back_populates="users")
    files: Mapped[list["Files"]] = relationship(back_populates="owner")


class Files(Base):
    __tablename__ = "files"
    __table_args__ = (
        # Чтобы не повторить для одной роли то же право
        UniqueConstraint(
            "user_id",
            "name",
            name="uq_user_file_name"
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str]
    content: Mapped[str]

    owner: Mapped["Users"] = relationship(back_populates="files")
