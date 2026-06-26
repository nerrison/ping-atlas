from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.endpoint import Endpoint
from app.models.group import Group
from app.schemas.endpoint import EndpointCreate, EndpointUpdate


class EndpointRepository:

    def get_by_id(self, db: Session, id: UUID):
        return db.get(Endpoint, id)

    def get_group_by_id(self, db: Session, id: UUID):
        return db.get(Group, id)

    def create(self, db: Session, data: EndpointCreate, group_id: UUID):
        endpoint = Endpoint(
            group_id=group_id,
            type=data.type,
            url=data.url,
            method=data.method,
            description=data.description,
        )

        db.add(endpoint)
        db.commit()
        db.refresh(endpoint)
        return endpoint

    def get(self, db: Session, group_id: UUID, id: UUID):
        stmt = select(Endpoint).where(
            Endpoint.id == id,
            Endpoint.group_id == group_id
        )
        return db.scalars(stmt).first()

    def list(self, db: Session, group_id: UUID):
        stmt = select(Endpoint).where(Endpoint.group_id == group_id)
        return db.scalars(stmt).all()

    def list_all(self, db: Session):
        stmt = select(Endpoint)
        return db.scalars(stmt).all()

    def patch(self, db: Session, data: EndpointUpdate, id: UUID):
        endpoint = db.get(Endpoint, id)
        if not endpoint:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(endpoint, key, value)

        db.commit()
        db.refresh(endpoint)
        return endpoint

    def put(self, db: Session, data: EndpointUpdate, id: UUID):
        endpoint = db.get(Endpoint, id)
        if not endpoint:
            return None

        endpoint.type = data.type or endpoint.type
        endpoint.url = data.url or endpoint.url
        endpoint.method = data.method or endpoint.method
        endpoint.description = data.description or endpoint.description

        db.commit()
        db.refresh(endpoint)
        return endpoint

    def delete(self, db: Session, id: UUID):
        endpoint = db.get(Endpoint, id)
        if not endpoint:
            return False

        db.delete(endpoint)
        db.commit()
        return True