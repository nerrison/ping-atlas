from uuid import UUID
from pydantic import BaseModel, ConfigDict


class GroupSearchResult(BaseModel):
    id: UUID
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


class EndpointSearchResult(BaseModel):
    id: UUID
    url: str
    method: str
    group_id: UUID

    model_config = ConfigDict(from_attributes=True)


class SearchResponse(BaseModel):
    groups: list[GroupSearchResult]
    endpoints: list[EndpointSearchResult]