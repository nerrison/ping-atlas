from sqlalchemy.orm import Session
from app.schemas.summary import EndpointSummary
from app.schemas.endpoint import EndpointCreate, EndpointDetail, EndpointResponse, EndpointUpdate
from app.repositories.endpoint import EndpointRepository

class EndpointService:
    def __init__(self, repo: EndpointRepository):
        self.repo = repo

    def list_endpoints_per_group(self, group_id):
        return self.repo.list(group_id)
    
    def get_endpoint(self, group_id, id):
        return self.repo.get(group_id, id)

    def list_endpoints(self):
        return self.repo.list_all()

    def create_endpoint(self, data: EndpointCreate, group_id):
        existing = self.repo.get_by_url(data.url, group_id)
        if existing:
            raise ValueError("Endpoint already exists in this group")

        return self.repo.create(data, group_id)

    def update_endpoint(self, data: EndpointUpdate, id):
        return self.repo.put(data,id)

    def patch_endpoint(self,data: EndpointUpdate,id):
        return self.repo.patch(data, id)

    def delete_endpoint(self, id):
        return self.repo.delete(id)