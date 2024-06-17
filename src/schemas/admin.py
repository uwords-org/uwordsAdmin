from typing import Optional
from datetime import datetime
from pydantic import EmailStr
from fastapi_users import schemas


class AdminRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class AdminCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    secret_key: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = True


class AdminUpdate(schemas.BaseUserUpdate):
    pass
