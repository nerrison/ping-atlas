from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IncidentBase(BaseModel):
    endpoint_id: UUID
    occurred_at: datetime
    error_message: str | None = None
    status_code: int | None = None

class IncidentCreate(IncidentBase):
    pass


class IncidentResponse(IncidentBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)