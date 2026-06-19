from uuid import UUID
from pydantic import BaseModel,Field


class EndpointSummary(BaseModel):
    id: UUID
    url: str
    method: str

    
class GroupSummary(BaseModel):
    id: UUID
    name: str
    slug: str

    endpoints: list[EndpointSummary] = Field(default_factory=list)