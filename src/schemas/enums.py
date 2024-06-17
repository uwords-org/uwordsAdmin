from enum import Enum


class MetricRange(str, Enum):
    today = "today"
    week = "week"
    month = "month"
    year = "year"
    alltime = "alltime"