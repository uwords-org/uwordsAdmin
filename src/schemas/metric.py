from datetime import datetime
from pydantic import BaseModel


class AdminGlobalMetric(BaseModel):
    id: int
    learned_words_amount: int
    learned_words_percents: int
    speech_seconds: int
    added_new_words: int
    added_all_words: int

    created_date: datetime


class AdminUserMetric(BaseModel):
    id: int
    learned_words_amount: int
    learned_words_percents: int
    speech_seconds: int
    added_new_words: int
    added_all_words: int

    user_id: int
    created_date: datetime
