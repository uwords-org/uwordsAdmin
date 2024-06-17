from datetime import datetime
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
            alltime_userwords_amount = today_metric.alltime_userwords_amount + metric.add_user_words_amount
            alltime_learned_amount = today_metric.alltime_learned_amount + metric.learned_amount
            
            today_userwords_amount = today_metric.today_userwords_amount + metric.add_user_words_amount
            today_learned_amount = today_metric.today_learned_amount + metric.learned_amount
        
            user_metric = {
                "alltime_userwords_amount": alltime_userwords_amount,
                "today_words_amount": today_metric.today_words_amount + metric.add_global_words_amount,
                "today_userwords_amount": today_userwords_amount,
                "alltime_learned_amount": alltime_learned_amount,
                "alltime_learned_percents": round(alltime_learned_amount / alltime_userwords_amount, 2),
                "today_learned_amount": today_learned_amount,
                "today_learned_percents": round(today_learned_amount / today_userwords_amount, 2),
                "alltime_speech_seconds": today_metric.alltime_speech_seconds + metric.speech_seconds,
                "alltime_video_seconds": today_metric.alltime_video_seconds + metric.video_seconds,
                "today_speech_seconds": today_metric.today_speech_seconds + metric.speech_seconds,
                "today_video_seconds": today_metric.today_video_seconds + metric.video_seconds
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
                alltime_userwords_amount = last_metric.alltime_userwords_amount + metric.add_user_words_amount
                alltime_learned_amount = last_metric.alltime_learned_amount + metric.learned_amount
                
                today_userwords_amount = last_metric.today_userwords_amount + metric.add_user_words_amount
                today_learned_amount = last_metric.today_learned_amount + metric.learned_amount

                user_metric = {
                    "alltime_userwords_amount": alltime_userwords_amount,
                    "today_words_amount": last_metric.today_words_amount + metric.add_global_words_amount,
                    "today_userwords_amount": today_userwords_amount,
                    "alltime_learned_amount": alltime_learned_amount,
                    "alltime_learned_percents": round(alltime_learned_amount / alltime_userwords_amount, 2),
                    "today_learned_amount": today_learned_amount,
                    "today_learned_percents": round(today_learned_amount / today_userwords_amount, 2),
                    "alltime_speech_seconds": last_metric.alltime_speech_seconds + metric.speech_seconds,
                    "alltime_video_seconds": last_metric.alltime_video_seconds + metric.video_seconds,
                    "today_speech_seconds": last_metric.today_speech_seconds + metric.speech_seconds,
                    "today_video_seconds": last_metric.today_video_seconds + metric.video_seconds,
                    "user_id": metric.user_id
                }

            else:
                user_metric = {
                    "alltime_userwords_amount": metric.add_user_words_amount,
                    "today_words_amount": metric.add_global_words_amount,
                    "today_userwords_amount": metric.add_user_words_amount,
                    "alltime_learned_amount": metric.learned_amount,
                    "alltime_learned_percents": round(metric.learned_amount / metric.add_user_words_amount, 2),
                    "today_learned_amount": metric.learned_amount,
                    "today_learned_percents": round(metric.learned_amount / metric.add_user_words_amount, 2),
                    "alltime_speech_seconds": metric.speech_seconds,
                    "alltime_video_seconds": metric.video_seconds,
                    "today_speech_seconds": metric.speech_seconds,
                    "today_video_seconds": metric.video_seconds,
                    "user_id": metric.user_id
                }
            
            return await self.repo.add_one(
                data=user_metric
            )
    
    async def get_metric(self, user_id: str, metric_range: MetricRange) -> UserMetric:
        today = datetime.today()

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
                date = datetime(2020, 1, 1)

        return await self.repo.get_all_by_filter(
            filters=(
                UserMetric.user_id == user_id, 
                UserMetric.created_date >= datetime(date.year, date.month, date.day),
            ),
            order=UserMetric.id.asc(),
            limit=0
        )
