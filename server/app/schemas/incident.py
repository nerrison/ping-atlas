from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class IncidentBase(BaseModel):
    endpoint_url: str | None = None
    incident_time: datetime | None = None
    error_msg: str | None = None
    status: str | None = None
    last_status_code: int | None = None


class IncidentCreate(IncidentBase):
    endpoint_id: UUID


class IncidentUpdate(BaseModel):
    endpoint_url: str | None = None
    incident_time: datetime | None = None
    error_msg: str | None = None
    status: str | None = None
    last_status_code: int | None = None


class IncidentResponse(IncidentBase):
    id: UUID
    endpoint_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)