from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class DumpGlobalMetricSchema(BaseModel):
    id: int
    created_date: datetime

    alltime_words_amount: int
    alltime_userwords_amount: int
    today_words_amount: int
    today_userwords_amount: int
    alltime_learned_amount: int
    alltime_learned_percents: float
    today_learned_amount: int
    today_learned_percents: float
    alltime_speech_seconds: int
    alltime_video_seconds: int
    today_speech_seconds: int
    today_video_seconds: int


class DumpUserMetricSchema(BaseModel):
    id: int
    user_id: str
    created_date: datetime

    alltime_userwords_amount: int
    today_words_amount: int
    today_userwords_amount: int
    alltime_learned_amount: int
    alltime_learned_percents: float
    today_learned_amount: int
    today_learned_percents: float
    alltime_speech_seconds: int
    alltime_video_seconds: int
    today_speech_seconds: int
    today_video_seconds: int


class PostMetricSchema(BaseModel):
    user_id: str

    add_global_words_amount: int
    add_user_words_amount: int
    learned_amount: int
    speech_seconds: int
    video_seconds: int
