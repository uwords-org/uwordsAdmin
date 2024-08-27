from sqlalchemy import Column, Integer, String, DateTime, func, Float

from src.database.db_config import Base


class GlobalMetric(Base):
    __tablename__ = "global_metric"

    id = Column(Integer, primary_key=True, index=True)

    alltime_words_amount = Column(Integer, nullable=True, default=0)
    alltime_userwords_amount = Column(Integer, nullable=True, default=0)

    alltime_learned_amount = Column(Integer, nullable=True, default=0)
    alltime_learned_percents = Column(Float, nullable=True, default=0)

    alltime_speech_seconds = Column(Integer, nullable=True, default=0)
    alltime_video_seconds = Column(Integer, nullable=True, default=0)

    words_amount = Column(Integer, nullable=True, default=0)
    userwords_amount = Column(Integer, nullable=True, default=0)

    learned_amount = Column(Integer, nullable=True, default=0)
    learned_percents = Column(Float, nullable=True, default=0)

    speech_seconds = Column(Integer, nullable=True, default=0)
    video_seconds = Column(Integer, nullable=True, default=0)

    created_date = Column(DateTime(timezone=True), server_default=func.now())


class UserMetric(Base):
    __tablename__ = "user_metric"

    id = Column(Integer, primary_key=True, index=True)

    alltime_userwords_amount = Column(Integer, nullable=True, default=0)

    alltime_learned_amount = Column(Integer, nullable=True, default=0)
    alltime_learned_percents = Column(Float, nullable=True, default=0)

    alltime_speech_seconds = Column(Integer, nullable=True, default=0)
    alltime_video_seconds = Column(Integer, nullable=True, default=0)

    words_amount = Column(Integer, nullable=True, default=0)
    userwords_amount = Column(Integer, nullable=True, default=0)

    learned_amount = Column(Integer, nullable=True, default=0)
    learned_percents = Column(Float, nullable=True, default=0)
    
    speech_seconds = Column(Integer, nullable=True, default=0)
    video_seconds = Column(Integer, nullable=True, default=0)
    
    uwords_uid = Column(String, nullable=False)

    created_date = Column(DateTime(timezone=True), server_default=func.now())
