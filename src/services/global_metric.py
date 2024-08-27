from datetime import datetime
from typing import Optional, Union
from dateutil.relativedelta import relativedelta

from src.schemas.enums import MetricRange
from src.database.models import GlobalMetric
from src.schemas.metric import PostMetricSchema
from src.utils.repository import AbstractRepository


class GlobalMetricService:
    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def update_or_create_metric(self, metric: PostMetricSchema) -> GlobalMetric:
        today = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        
        # Проверка существующей метрики за сегодня
        today_metric: GlobalMetric = await self.repo.get_one(
            filters=(GlobalMetric.created_date >= today,)
        )

        # Если сегодняшняя метрика существует, инкрементируем значения
        if today_metric:
            updated_values = self._increment_metric(existing_metric=today_metric, new_metric=metric)
            return await self.repo.update_one(
                id=today_metric.id,
                values=updated_values
            )
        
        # Если метрики за сегодня нет, используем последнюю метрику для накопительных значений
        else:
            last_metric: GlobalMetric = await self.repo.get_last(filters=None)
            if last_metric:
                new_values = self._initialize_metric_with_previous(last_metric=last_metric, new_metric=metric)
            else:
                new_values = self._initialize_first_metric(new_metric=metric)

            return await self.repo.add_one(data=new_values)

    def _increment_metric(self, existing_metric: GlobalMetric, new_metric: PostMetricSchema) -> dict:
        """
        Инкрементирует значения существующей метрики с новыми данными.
        """
        alltime_userwords_amount = existing_metric.alltime_userwords_amount + new_metric.add_userwords_amount
        alltime_learned_amount = existing_metric.alltime_learned_amount + new_metric.learned_amount
        userwords_amount = existing_metric.userwords_amount + new_metric.add_userwords_amount
        learned_amount = existing_metric.learned_amount + new_metric.learned_amount

        alltime_learned_percents = self._calculate_percentage(part=alltime_learned_amount, whole=alltime_userwords_amount)
        learned_percents = self._calculate_percentage(part=learned_amount, whole=alltime_userwords_amount)

        return {
            "alltime_words_amount": existing_metric.alltime_words_amount + new_metric.add_words_amount,
            "alltime_userwords_amount": alltime_userwords_amount,
            "alltime_learned_amount": alltime_learned_amount,
            "alltime_learned_percents": alltime_learned_percents,
            "alltime_speech_seconds": existing_metric.alltime_speech_seconds + new_metric.speech_seconds,
            "alltime_video_seconds": existing_metric.alltime_video_seconds + new_metric.video_seconds,
            "words_amount": existing_metric.words_amount + new_metric.add_words_amount,
            "userwords_amount": userwords_amount,
            "learned_amount": learned_amount,
            "learned_percents": learned_percents,
            "speech_seconds": existing_metric.speech_seconds + new_metric.speech_seconds,
            "video_seconds": existing_metric.video_seconds + new_metric.video_seconds
        }

    def _initialize_metric_with_previous(self, last_metric: GlobalMetric, new_metric: PostMetricSchema) -> dict:
        """
        Создает новую метрику на основе последней существующей метрики и новых данных.
        """
        alltime_userwords_amount = last_metric.alltime_userwords_amount + new_metric.add_userwords_amount
        alltime_learned_amount = last_metric.alltime_learned_amount + new_metric.learned_amount

        alltime_learned_percents = self._calculate_percentage(part=alltime_learned_amount, whole=alltime_userwords_amount)
        learned_percents = self._calculate_percentage(part=new_metric.learned_amount, whole=new_metric.add_userwords_amount)

        return {
            "alltime_words_amount": last_metric.alltime_words_amount + new_metric.add_words_amount,
            "alltime_userwords_amount": alltime_userwords_amount,
            "alltime_learned_amount": alltime_learned_amount,
            "alltime_learned_percents": alltime_learned_percents,
            "alltime_speech_seconds": last_metric.alltime_speech_seconds + new_metric.speech_seconds,
            "alltime_video_seconds": last_metric.alltime_video_seconds + new_metric.video_seconds,
            "words_amount": new_metric.add_words_amount,
            "userwords_amount": new_metric.add_userwords_amount,
            "learned_amount": new_metric.learned_amount,
            "learned_percents": learned_percents,
            "speech_seconds": new_metric.speech_seconds,
            "video_seconds": new_metric.video_seconds
        }

    def _initialize_first_metric(self, new_metric: PostMetricSchema) -> dict:
        """
        Создает первую метрику, если в базе данных ещё нет данных.
        """
        alltime_learned_percents = self._calculate_percentage(part=new_metric.learned_amount, whole=new_metric.add_userwords_amount)
        learned_percents = alltime_learned_percents

        return {
            "alltime_words_amount": new_metric.add_words_amount,
            "alltime_userwords_amount": new_metric.add_userwords_amount,
            "alltime_learned_amount": new_metric.learned_amount,
            "alltime_learned_percents": alltime_learned_percents,
            "alltime_speech_seconds": new_metric.speech_seconds,
            "alltime_video_seconds": new_metric.video_seconds,
            "words_amount": new_metric.add_words_amount,
            "userwords_amount": new_metric.add_userwords_amount,
            "learned_amount": new_metric.learned_amount,
            "learned_percents": learned_percents,
            "speech_seconds": new_metric.speech_seconds,
            "video_seconds": new_metric.video_seconds
        }

    def _calculate_percentage(self, part: float, whole: float) -> float:
        """
        Вычисляет процентную долю part от whole.
        """
        return round((part / whole) * 100, 2) if whole != 0 else 0.0
    
    async def get_metric(
        self, 
        is_union: bool, 
        metric_range: MetricRange, 
        date_from: Optional[datetime] = None, 
        date_to: Optional[datetime] = None
    ) -> Union[GlobalMetric, list[GlobalMetric], dict]:
        today = datetime.today()
        
        # Определение даты начала фильтрации на основе metric_range
        date = self._get_start_date_based_on_range(metric_range, today)

        filters = []
        if date:
            filters.append(GlobalMetric.created_date >= datetime(date.year, date.month, date.day))
        if date_from:
            filters.append(GlobalMetric.created_date >= datetime(date_from.year, date_from.month, date_from.day))
        if date_to:
            filters.append(GlobalMetric.created_date <= datetime(date_to.year, date_to.month, date_to.day))
        if not date_from and not date_to and not date:
            filters.append(GlobalMetric.created_date >= datetime(today.year, today.month, today.day))

        metrics: list[GlobalMetric] = await self.repo.get_all_by_filter(
            filters=tuple(filters),
            order=GlobalMetric.id.asc(),
            limit=0
        )

        if is_union:
            return self._aggregate_metrics(metrics)
        
        return metrics

    def _get_start_date_based_on_range(self, metric_range: MetricRange, today: datetime) -> Optional[datetime]:
        """Определяет начальную дату на основе указанного диапазона метрик."""
        
        if metric_range and metric_range != MetricRange.no_range:
            match metric_range:
                case MetricRange.today:
                    return today
                case MetricRange.week:
                    return today - relativedelta(weeks=1)
                case MetricRange.month:
                    return today - relativedelta(months=1)
                case MetricRange.year:
                    return today - relativedelta(years=1)
                case MetricRange.alltime:
                    return datetime(2000, 1, 1)
        return None

    def _aggregate_metrics(self, metrics: list[GlobalMetric]) -> dict:
        """Агрегирует список метрик в один словарь с накопленными значениями."""

        if not metrics:
            return {}  # Возвращаем пустой словарь, если метрик нет
        
        output_json = {
            "created_date": metrics[-1].created_date,
            "alltime_words_amount": metrics[-1].alltime_words_amount,
            "alltime_userwords_amount": metrics[-1].alltime_userwords_amount,
            "alltime_learned_amount": metrics[-1].alltime_learned_amount,
            "alltime_learned_percents": metrics[-1].alltime_learned_percents,
            "alltime_speech_seconds": metrics[-1].alltime_speech_seconds,
            "alltime_video_seconds": metrics[-1].alltime_video_seconds,
            "words_amount": 0,
            "userwords_amount": 0,
            "learned_amount": 0,
            "learned_percents": 0,
            "speech_seconds": 0,
            "video_seconds": 0
        }

        for metric in metrics:
            output_json["words_amount"] += metric.words_amount
            output_json["userwords_amount"] += metric.userwords_amount
            output_json["learned_amount"] += metric.learned_amount
            output_json["speech_seconds"] += metric.speech_seconds
            output_json["video_seconds"] += metric.video_seconds

        if output_json["userwords_amount"] > 0:
            output_json["learned_percents"] = round(
                (output_json["learned_amount"] / output_json["userwords_amount"]) * 100, 2
            )
        else:
            output_json["learned_percents"] = 0

        return output_json