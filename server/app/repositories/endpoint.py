from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.endpoint import Endpoint
from app.models.group import Group
from app.schemas.endpoint import EndpointCreate, EndpointUpdate, EndpointPut


class EndpointRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_by_id(self, id: UUID):
        return self.db.get(Endpoint, id)

    def get_group_by_id(self, id: UUID):
        return self.db.get(Group, id)
    
    def get_by_url(self, url: str, group_id:UUID):
        stmt = select(Endpoint).where(Endpoint.url == url, Endpoint.group_id==group_id)
        return self.db.scalars(stmt).first()

    def create(self, data: EndpointCreate, group_id: UUID):
        endpoint = Endpoint(
            group_id=group_id,
            name = data.name,
            type=data.type,
            url=data.url,
            method=data.method,
            description=data.description,
        )

        self.db.add(endpoint)
        return endpoint

    def get(self, id: UUID):
        stmt = select(Endpoint).where(
            Endpoint.id == id,
        )
        return self.db.scalars(stmt).first()

    def list(self, group_id: UUID):
        stmt = select(Endpoint).where(Endpoint.group_id == group_id)
        return self.db.scalars(stmt).all()

    def list_all(self):
        stmt = select(Endpoint)
        return self.db.scalars(stmt).all()

    def patch(self, data: EndpointUpdate, id: UUID):
        endpoint = self.db.get(Endpoint, id)
        if not endpoint:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(endpoint, key, value)

        return endpoint

    def put(self, data: EndpointPut, id: UUID):
        endpoint = self.db.get(Endpoint, id)

        if not endpoint:
            return None

        if data.name is not None:
            endpoint.name = data.name

        if data.type is not None:
            endpoint.type = data.type

        if data.url is not None:
            endpoint.url = data.url

        if data.method is not None:
            endpoint.method = data.method

        if data.description is not None:
            endpoint.description = data.description

        return endpoint

    def delete(self, id: UUID):
        endpoint = self.db.get(Endpoint, id)
        if not endpoint:
            return False

        self.db.delete(endpoint)

        return True