from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .endpoint import EndpointResponse


class GroupBase(BaseModel):
    name: str
    slug: str
    type: Optional[str] = None
    description: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None


class GroupResponse(GroupBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

