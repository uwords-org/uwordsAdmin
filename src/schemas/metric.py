from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class DumpGlobalMetricSchema(BaseModel):
    created_date: datetime

    alltime_words_amount: int
    alltime_userwords_amount: int
    alltime_learned_amount: int
    alltime_learned_percents: float
    alltime_speech_seconds: int
    alltime_video_seconds: int
    words_amount: int
    userwords_amount: int
    learned_amount: int
    learned_percents: float
    speech_seconds: int
    video_seconds: int


class DumpUserMetricSchema(BaseModel):
    uwords_uid: str
    created_date: datetime

    alltime_userwords_amount: int
    alltime_learned_amount: int
    alltime_learned_percents: float
    alltime_speech_seconds: int
    alltime_video_seconds: int
    words_amount: int
    userwords_amount: int
    learned_amount: int
    learned_percents: float
    speech_seconds: int
    video_seconds: int


class PostMetricSchema(BaseModel):
    uwords_uid: str

    add_words_amount: Optional[int] = 0
    add_userwords_amount: Optional[int] = 0
    learned_amount: Optional[int] = 0
    speech_seconds: Optional[int] = 0
    video_seconds: Optional[int] = 0
