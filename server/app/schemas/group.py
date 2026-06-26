from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GroupBase(BaseModel):
    name: str
    slug: str
    type: str | None = None
    description: str | None = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    type: str | None = None
    description: str | None = None


class GroupResponse(GroupBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)