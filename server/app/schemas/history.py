from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class HistoryCreate(BaseModel):
    endpoint_id: UUID

    latency: int
    availability: float
    errors: int = 0

    timestamp: datetime

class HistoryResponse(BaseModel):
    id: UUID
    endpoint_id: UUID

    latency: int
    availability: float
    errors: int

    timestamp: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MetricPoint(BaseModel):
    timestamp: datetime
    latency: int
    availability: float
    errors: int

class HistoryRange(BaseModel):
    points: list[MetricPoint]

class HistoryChartResponse(BaseModel):
    history: dict[str, HistoryRange]