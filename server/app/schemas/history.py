from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HistoryCreate(BaseModel):

    latency: int
    availability: float
    error: int = 0

    check_time: datetime


class HistoryResponse(BaseModel):
    id: UUID
    endpoint_id: UUID

    latency: int
    availability: float
    error: int

    check_time: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MetricPoint(BaseModel):
    check_time: datetime
    latency: int
    availability: float
    error: int


class HistoryRange(BaseModel):
    points: list[MetricPoint]


class HistoryChartResponse(BaseModel):
    history: dict[str, HistoryRange]