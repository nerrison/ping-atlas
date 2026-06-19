from uuid import UUID
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from .history import HistoryResponse
from .incident import IncidentResponse


EndpointStatus = Literal["UP", "DOWN", "DEGRADED"]

HTTPMethod = Literal[
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE"
]


class EndpointBase(BaseModel):
    type: str | None = None
    url: str
    description: str | None = None
    method: HTTPMethod


class EndpointCreate(EndpointBase):
    group_id: UUID


class EndpointUpdate(BaseModel):
    type: str | None = None
    url: str | None = None
    description: str | None = None
    method: HTTPMethod | None = None


class EndpointResponse(EndpointBase):
    id: UUID
    group_id: UUID

    status: EndpointStatus
    response_time: int | None = None
    last_timestamp: datetime | None = None
    uptime: int | None = None

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EndpointDetail(BaseModel):
    endpoint: EndpointResponse

    history: list[HistoryResponse]
    incidents: list[IncidentResponse]

    model_config = ConfigDict(from_attributes=True)