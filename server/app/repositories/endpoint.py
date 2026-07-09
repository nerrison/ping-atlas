from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.endpoint import Endpoint
from app.models.group import Group
from app.schemas.endpoint import EndpointCreate, EndpointUpdate


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
        self.db.commit()
        self.db.refresh(endpoint)
        return endpoint

    def get(self, group_id: UUID, id: UUID):
        stmt = select(Endpoint).where(
            Endpoint.id == id,
            Endpoint.group_id == group_id
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

        self.db.commit()
        self.db.refresh(endpoint)
        return endpoint

    def put(self, data: EndpointUpdate, id: UUID):
        endpoint = self.db.get(Endpoint, id)
        if not endpoint:
            return None

        endpoint.type = data.type or endpoint.type
        endpoint.url = data.url or endpoint.url
        endpoint.method = data.method or endpoint.method
        endpoint.description = data.description or endpoint.description

        self.db.commit()
        self.db.refresh(endpoint)
        return endpoint

    def delete(self, id: UUID):
        endpoint = self.db.get(Endpoint, id)
        if not endpoint:
            return False

        self.db.delete(endpoint)
        self.db.commit()
        return True