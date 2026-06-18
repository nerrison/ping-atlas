from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Literal


class EndpointBase(BaseModel):
    type: str | None = None
    url: str
    description: str | None = None
    method: str

    status: Literal["UP", "DOWN", "DEGRADED"]


class EndpointCreate(EndpointBase):
    group_id: UUID


class EndpointUpdate(BaseModel):
    type: str | None = None
    url: str | None = None
    description: str | None = None
    method: str | None = None
    status: Literal["UP", "DOWN", "DEGRADED"] | None = None
    response_time: int | None = None
    last_check: datetime | None = None
    uptime: int | None = None


class EndpointResponse(EndpointBase):
    id: UUID
    group_id: UUID

    response_time: int | None = None
    last_check: datetime | None = None
    uptime: int | None = None

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)