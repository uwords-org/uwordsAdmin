from src.repositories.reps import GlobalMetricRepository, UserMetricRepository
from src.services.global_metric import GlobalMetricService
from src.services.user_metric import UserMetricService


def global_metric_service_fabric():
    return GlobalMetricService(GlobalMetricRepository())


def user_metric_service_fabric():
    return UserMetricService(UserMetricRepository())
