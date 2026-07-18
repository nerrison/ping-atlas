from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IncidentBase(BaseModel):

    occurred_at: datetime
    ended_at:datetime | None

    occurred_at_status_code: int 
    ended_at_status_code: int | None = None

    error_message: str | None = None
    

class IncidentCreate(IncidentBase):
    pass


class IncidentResponse(IncidentBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)