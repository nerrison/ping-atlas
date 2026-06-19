from pydantic import BaseModel
from uuid import UUID


class GroupSearchResult(BaseModel):
    id: UUID
    name: str
    slug: str

class EndpointSearchResult(BaseModel):
    id: UUID
    url: str
    method: str
    group_id: UUID

class SearchResponse(BaseModel):
    groups: list[GroupSearchResult]
    endpoints: list[EndpointSearchResult]