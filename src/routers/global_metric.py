from datetime import datetime
from typing import Annotated, List, Optional, Union
from fastapi import APIRouter, Depends
from src.schemas.enums import MetricRange
from src.schemas.metric import DumpGlobalMetricSchema
from src.services.global_metric import GlobalMetricService
from src.utils.dependencies import global_metric_service_fabric
from src.utils.headers import check_service_token

router_v1 = APIRouter(prefix="/api/v1/metric", tags=["Global Metric"])


@router_v1.get(
    path="/global", 
    response_model=Union[List[DumpGlobalMetricSchema], DumpGlobalMetricSchema], 
    summary='Получение метрики по дням', 
    description="Ответ приходит в виде списка по дням в указанном диапазоне"
)
async def get_global_metric(
    global_session_service: Annotated[GlobalMetricService, Depends(global_metric_service_fabric)],
    is_union: bool,
    metric_range: MetricRange,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    token = Depends(check_service_token)
):
    return await global_session_service.get_metric(
        metric_range=metric_range,
        is_union=is_union,
        date_from=date_from,
        date_to=date_to
    )
