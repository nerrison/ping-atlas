class EndpointSummary(BaseModel):
    id: UUID
    url: str

    model_config = ConfigDict(from_attributes=True)


class GroupWithEndpoints(GroupResponse):
    endpoints: list[EndpointSummary] = []