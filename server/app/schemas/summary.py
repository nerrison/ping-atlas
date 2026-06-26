from uuid import UUID
from pydantic import BaseModel,ConfigDict, Field


class EndpointSummary(BaseModel):
    id: UUID
    url: str
    method: str

    model_config = ConfigDict(from_attributes=True)

    
class GroupSummary(BaseModel):
    id: UUID
    name: str
    slug: str

    endpoints: list[EndpointSummary] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)