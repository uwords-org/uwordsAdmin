from enum import Enum


class MetricRange(str, Enum):
    no_range = "no_range"
    today = "today"
    week = "week"
    month = "month"
    year = "year"
    alltime = "alltime"