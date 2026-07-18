from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .history import HistoryResponse
from .incident import IncidentResponse

from enum import StrEnum


class EndpointStatus(StrEnum):
    UP = "UP"
    DOWN = "DOWN"
    DEGRADED = "DEGRADED"


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class EndpointBase(BaseModel):
    name: str
    type: str
    url: str
    description: str | None = None
    method: HttpMethod

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator("method", mode="before")
    @classmethod
    def normalize_method(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


class EndpointCreate(EndpointBase):
    pass


class EndpointUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    url: str | None = None
    description: str | None = None
    method: HttpMethod | None = None

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator("method", mode="before")
    @classmethod
    def normalize_method(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


class EndpointPut(BaseModel):
    name: str
    type: str | None
    url: str
    description: str | None
    method: HttpMethod

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator("method", mode="before")
    @classmethod
    def normalize_method(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value