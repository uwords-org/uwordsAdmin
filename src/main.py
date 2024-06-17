from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware

from src.database.db_config import Admin
from src.schemas.admin import AdminCreate, AdminRead
from src.utils.admin import get_admin_manager, auth_backend


app = FastAPI(
    title="UWords FastAPI Admin",
    description="API of UWords Admin Panel",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_admins = FastAPIUsers[Admin, int](
    get_admin_manager,
    [auth_backend],
)

app.include_router(
    fastapi_admins.get_auth_router(auth_backend),
    prefix="/admin/auth",
    tags=["Admin Auth"],
)

app.include_router(
    fastapi_admins.get_register_router(AdminRead, AdminCreate),
    prefix="/admin/auth",
    tags=["Admin Auth"],
)
