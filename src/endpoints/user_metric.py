from typing import Annotated, List
from fastapi import APIRouter, Depends

from src.schemas.enums import MetricRange
from src.services.user_metric import UserMetricService
from src.services.global_metric import GlobalMetricService
from src.schemas.metric import PostMetricSchema, DumpUserMetricSchema
from src.utils.dependencies import global_metric_service_fabric, user_metric_service_fabric

router_v1 = APIRouter(prefix="/api/v1/metric", tags=["User Metric"])


@router_v1.get("/user", response_model=List[DumpUserMetricSchema], summary='Получение метрики по дням')
async def get_user_metric(
    user_session_service: Annotated[UserMetricService, Depends(user_metric_service_fabric)],
    metric_range: MetricRange,
    user_id: str
):
    return await user_session_service.get_metric(user_id=user_id, metric_range=metric_range)


@router_v1.post("/user", response_model=DumpUserMetricSchema, summary='Обновление метрики')
async def update_user_metric(
    metric: PostMetricSchema,
    user_session_service: Annotated[UserMetricService, Depends(user_metric_service_fabric)],
    global_session_service: Annotated[GlobalMetricService, Depends(global_metric_service_fabric)]
):
    
    await global_session_service.update_or_create_metric(metric=metric)
    return await user_session_service.update_or_create_metric(metric=metric)
