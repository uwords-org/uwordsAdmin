from typing import Annotated, List
from fastapi import APIRouter, Depends
from src.schemas.enums import MetricRange
from src.schemas.metric import DumpGlobalMetricSchema
from src.services.global_metric import GlobalMetricService
from src.utils.dependencies import global_metric_service_fabric

router_v1 = APIRouter(prefix="/api/v1/metric", tags=["Global Metric"])


@router_v1.get(path="/global", response_model=List[DumpGlobalMetricSchema], summary='Получение метрики по дням', description="Ответ приходит в виде списка по дням в указанном диапазоне")
async def get_global_metric(
    global_session_service: Annotated[GlobalMetricService, Depends(global_metric_service_fabric)],
    metric_range: MetricRange
):
    return await global_session_service.get_metric(metric_range=metric_range)
