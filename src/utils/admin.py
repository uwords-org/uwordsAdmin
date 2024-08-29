from typing import Optional
from fastapi import Depends, Request

from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, schemas, models

from src.database.db_config import Admin, get_admin_db
from src.config.instance import FASTAPI_SECRET, ADMIN_SECRET


bearer_transport = BearerTransport(tokenUrl="")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=FASTAPI_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy
)


class AdminManager(IntegerIDMixin, BaseUserManager[Admin, int]):
    reset_password_token_secret = FASTAPI_SECRET
    verification_token_secret = FASTAPI_SECRET

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        secret_key = user_dict.pop("secret_key")

        if secret_key == ADMIN_SECRET:
            user_dict["is_superuser"] = True

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_register(self, admin: Admin, request: Optional[Request] = None):
        print(f"Admin {admin.id} has registered.")

    async def on_after_forgot_password(
        self, admin: Admin, token: str, request: Optional[Request] = None
    ):
        print(f"Admin {admin.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, admin: Admin, token: str, request: Optional[Request] = None
    ):
        print(
            f"Verification requested for admin {admin.id}. Verification token: {token}"
        )


async def get_admin_manager(admin_db=Depends(get_admin_db)):
    yield AdminManager(admin_db)
