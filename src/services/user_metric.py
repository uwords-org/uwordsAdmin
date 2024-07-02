from datetime import datetime
from typing import Optional
from src.schemas.enums import MetricRange
from dateutil.relativedelta import relativedelta
from src.schemas.metric import PostMetricSchema
from src.utils.repository import AbstractRepository
from src.database.models import UserMetric


class UserMetricService:
    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def update_or_create_metric(self, metric: PostMetricSchema) -> UserMetric:
        
        today = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        today_metric: UserMetric = await self.repo.get_one(
            filters=(
                UserMetric.user_id == metric.user_id,
                UserMetric.created_date >= today
            )
        )

        if today_metric:
            alltime_userwords_amount = today_metric.alltime_userwords_amount + metric.add_userwords_amount
            alltime_learned_amount = today_metric.alltime_learned_amount + metric.learned_amount
            
            userwords_amount = today_metric.userwords_amount + metric.add_userwords_amount
            learned_amount = today_metric.learned_amount + metric.learned_amount
        
            user_metric = {
                "alltime_userwords_amount": alltime_userwords_amount,
                "alltime_learned_amount": alltime_learned_amount,
                "alltime_learned_percents": round((alltime_learned_amount / alltime_userwords_amount) * 100, 2),
                "alltime_speech_seconds": today_metric.alltime_speech_seconds + metric.speech_seconds,
                "alltime_video_seconds": today_metric.alltime_video_seconds + metric.video_seconds,
                "words_amount": today_metric.words_amount + metric.add_words_amount,
                "userwords_amount": userwords_amount,
                "learned_amount": learned_amount,
                "learned_percents": round((learned_amount / alltime_userwords_amount) * 100, 2),
                "speech_seconds": today_metric.speech_seconds + metric.speech_seconds,
                "video_seconds": today_metric.video_seconds + metric.video_seconds
            }
            
            return await self.repo.update_one(
                id=today_metric.id,
                values=user_metric
            )
        
        else:
            last_metric: UserMetric = await self.repo.get_last(
                filters=(
                    UserMetric.user_id == metric.user_id,
                )
            )

            if last_metric:
                alltime_userwords_amount = last_metric.alltime_userwords_amount + metric.add_userwords_amount
                alltime_learned_amount = last_metric.alltime_learned_amount + metric.learned_amount
                
                userwords_amount = last_metric.userwords_amount + metric.add_userwords_amount
                learned_amount = last_metric.learned_amount + metric.learned_amount

                user_metric = {
                    "alltime_userwords_amount": alltime_userwords_amount,
                    "alltime_learned_amount": alltime_learned_amount,
                    "alltime_learned_percents": round((alltime_learned_amount / alltime_userwords_amount) * 100, 2),
                    "alltime_speech_seconds": last_metric.alltime_speech_seconds + metric.speech_seconds,
                    "alltime_video_seconds": last_metric.alltime_video_seconds + metric.video_seconds,
                    "words_amount": last_metric.words_amount + metric.add_words_amount,
                    "userwords_amount": userwords_amount,
                    "learned_amount": learned_amount,
                    "learned_percents": round((learned_amount / alltime_userwords_amount) * 100, 2),
                    "speech_seconds": last_metric.speech_seconds + metric.speech_seconds,
                    "video_seconds": last_metric.video_seconds + metric.video_seconds,
                    "user_id": metric.user_id
                }

            else:
                user_metric = {
                    "alltime_userwords_amount": metric.add_userwords_amount,
                    "alltime_learned_amount": metric.learned_amount,
                    "alltime_learned_percents": round((metric.learned_amount / metric.add_userwords_amount) * 100, 2),
                    "alltime_speech_seconds": metric.speech_seconds,
                    "alltime_video_seconds": metric.video_seconds,
                    "words_amount": metric.add_words_amount,
                    "userwords_amount": metric.add_userwords_amount,
                    "learned_amount": metric.learned_amount,
                    "learned_percents": round((metric.learned_amount / metric.add_userwords_amount) * 100, 2),
                    "speech_seconds": metric.speech_seconds,
                    "video_seconds": metric.video_seconds,
                    "user_id": metric.user_id
                }
            
            return await self.repo.add_one(
                data=user_metric
            )
    
    async def get_metric(self, user_id: str, is_union: bool, metric_range: MetricRange, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> UserMetric:
        today = datetime.today()

        if metric_range and metric_range != MetricRange.no_range:
            match metric_range:
                case MetricRange.today:
                    date = today
                case MetricRange.week:
                    date = today - relativedelta(weeks=1)
                case MetricRange.month:
                    date = today - relativedelta(months=1)
                case MetricRange.year:
                    date = today - relativedelta(years=1)
                case MetricRange.alltime:
                    date = datetime(2000, 1, 1)
            
            metrics: list[UserMetric] = await self.repo.get_all_by_filter(
                filters=(
                    UserMetric.user_id == user_id,
                    UserMetric.created_date >= datetime(date.year, date.month, date.day),
                ),
                order=UserMetric.id.asc(),
                limit=0
            )
        
        elif date_from and not date_to:
            metrics: list[UserMetric] = await self.repo.get_all_by_filter(
                filters=(
                    UserMetric.user_id == user_id, 
                    UserMetric.created_date >= datetime(date_from.year, date_from.month, date_from.day),
                ),
                order=UserMetric.id.asc(),
                limit=0
            )
        
        elif date_from and date_to:
            metrics: list[UserMetric] = await self.repo.get_all_by_filter(
                filters=(
                    UserMetric.user_id == user_id, 
                    UserMetric.created_date >= datetime(date_from.year, date_from.month, date_from.day),
                    UserMetric.created_date <= datetime(date_to.year, date_to.month, date_to.day),
                ),
                order=UserMetric.id.asc(),
                limit=0
            )
        
        elif not date_from and date_to:
            metrics: list[UserMetric] = await self.repo.get_all_by_filter(
                filters=(
                    UserMetric.user_id == user_id, 
                    UserMetric.created_date <= datetime(date_to.year, date_to.month, date_to.day),
                ),
                order=UserMetric.id.asc(),
                limit=0
            )
        
        else:
            metrics: list[UserMetric] = await self.repo.get_all_by_filter(
                filters=(
                    UserMetric.user_id == user_id, 
                    UserMetric.created_date >= datetime(today.year, today.month, today.day),
                ),
                order=UserMetric.id.asc(),
                limit=0
            )

        if is_union:
            output_json = {
                "user_id": metrics[-1].user_id,
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
            
            output_json["learned_percents"] = round((output_json["learned_amount"] / output_json["userwords_amount"]) * 100, 2)

            return output_json
    
        else:
            return metrics
