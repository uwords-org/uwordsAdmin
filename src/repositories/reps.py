from src.utils.repository import SQLAlchemyRepository
from src.database.models import GlobalMetric, UserMetric


class GlobalMetricRepository(SQLAlchemyRepository):
    model = GlobalMetric


class UserMetricRepository(SQLAlchemyRepository):
    model = UserMetric
