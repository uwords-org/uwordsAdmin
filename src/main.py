from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware

from src.database.db_config import Admin
from src.schemas.admin import AdminCreate, AdminRead
from src.utils.admin import get_admin_manager, auth_backend

from src.endpoints.global_metric import router_v1 as global_metric_router
from src.endpoints.user_metric import router_v1 as user_metric_router


app = FastAPI(
    title="UWords FastAPI Admin",
    description="API of UWords Admin Panel",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_admins = FastAPIUsers[Admin, int](
    get_admin_manager,
    [auth_backend],
)

app.include_router(
    fastapi_admins.get_auth_router(auth_backend),
    prefix="/api/v1/admin/auth",
    tags=["Admin Auth"],
)

app.include_router(
    fastapi_admins.get_register_router(AdminRead, AdminCreate),
    prefix="/api/v1/admin/auth",
    tags=["Admin Auth"],
)

app.include_router(global_metric_router)
app.include_router(user_metric_router)