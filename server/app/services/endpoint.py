from sqlalchemy.orm import Session
from app.schemas.summary import EndpointSummary
from app.schemas.endpoint import EndpointCreate, EndpointDetail, EndpointResponse, EndpointUpdate
from app.repositories.endpoint import EndpointRepository

class EndpointService:
    def __init__(self):
        self.repo = EndpointRepository()
    
    def create_endpoint(self,db, data:EndpointCreate, group_ID):
        group_id = self.repo.get_group_by_id(db,group_ID)

        if not group_id:
            raise ValueError("Group doesn't exist")
        
        return self.repo.create(db, data, group_id)
    
    def get_endpoint(self, db, id):
        pass

    def list_endpoints(self, db):
        pass

    def update_endpoint(self, db, data, id):
        pass