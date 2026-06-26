from app.models.history import History
from app.schemas.history import MetricPoint


def to_metric_point(h: History) -> MetricPoint:
    return MetricPoint(
        check_time=h.check_time,
        latency=h.latency,
        availability=h.availability,
        error=h.error,
    )