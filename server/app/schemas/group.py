from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GroupBase(BaseModel):
    name: str
    type: str | None = None
    description: str | None = None


class GroupCreate(GroupBase):
    pass

class GroupUpdate(GroupBase):
    pass

class GroupPatch(BaseModel):
    name: str | None = None
    type: str | None = None
    description: str | None = None


class GroupResponse(GroupBase):
    id: UUID
    slug: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)