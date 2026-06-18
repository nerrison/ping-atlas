from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class HistoryBase(BaseModel):
    latency: int | None = None
    availability: int | None = None
    error: int | None = None
    check_time: datetime | None = None


class HistoryCreate(HistoryBase):
    endpoint_id: UUID


class HistoryUpdate(BaseModel):
    latency: int | None = None
    availability: int | None = None
    error: int | None = None
    check_time: datetime | None = None


class HistoryResponse(HistoryBase):
    id: UUID
    endpoint_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)