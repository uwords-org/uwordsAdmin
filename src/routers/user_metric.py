from datetime import datetime
from typing import Annotated, List, Optional, Union
from fastapi import APIRouter, Depends
from src.database.models import UserMetric
from src.schemas.enums import MetricRange
from src.services.user_metric import UserMetricService
from src.services.global_metric import GlobalMetricService
from src.schemas.metric import PostMetricSchema, DumpUserMetricSchema
from src.utils.dependencies import (
    global_metric_service_fabric,
    user_metric_service_fabric,
)
from src.utils.headers import check_service_token

router_v1 = APIRouter(prefix="/api/v1/metric", tags=["User Metric"])


@router_v1.get(
    "/user",
    summary="Получение метрики по дням",
    description="Ответ приходит в виде списка по дням в указанном диапазоне",
)
async def get_user_metric(
    user_metric_service: Annotated[
        UserMetricService, Depends(user_metric_service_fabric)
    ],
    uwords_uid: str,
    is_union: bool,
    metric_range: MetricRange,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    token=Depends(check_service_token),
):

    if not user_metric_service.repo.get_one(
        filters=[UserMetric.uwords_uid == uwords_uid]
    ):
        return await user_metric_service.update_or_create_metric(
            metric=PostMetricSchema(
                uwords_uid=uwords_uid,
                add_words_amount=0,
                add_userwords_amount=0,
                learned_amount=0,
                speech_seconds=0,
                video_seconds=0,
            )
        )

    return await user_metric_service.get_metric(
        uwords_uid=uwords_uid,
        metric_range=metric_range,
        is_union=is_union,
        date_from=date_from,
        date_to=date_to,
    )


@router_v1.post(
    "/user", response_model=DumpUserMetricSchema, summary="Обновление метрики"
)
async def update_user_metric(
    metric: PostMetricSchema,
    user_metric_service: Annotated[
        UserMetricService, Depends(user_metric_service_fabric)
    ],
    global_metric_service: Annotated[
        GlobalMetricService, Depends(global_metric_service_fabric)
    ],
    token=Depends(check_service_token),
):

    await global_metric_service.update_or_create_metric(metric=metric)
    return await user_metric_service.update_or_create_metric(metric=metric)
