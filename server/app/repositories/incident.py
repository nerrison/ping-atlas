from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from app.models.incident import Incident
from app.schemas.incident import IncidentCreate


class IncidentRepository:

    def get_by_id(self, db: Session, id: UUID):
        return db.get(Incident, id)

    def get_by_endpoint(self, db: Session, endpoint_id: UUID):
        stmt = (
            select(Incident)
            .where(Incident.endpoint_id == endpoint_id)
            .order_by(Incident.occurred_at.desc())
        )
        return db.scalars(stmt).all()

    def list(self, db: Session):
        return db.scalars(select(Incident)).all()

    def create(self, db: Session, data: IncidentCreate):
        incident = Incident(
            endpoint_id=data.endpoint_id,
            occurred_at=data.occurred_at,
            error_message=data.error_message,
            status_code=data.status_code,
        )

        db.add(incident)
        db.commit()
        db.refresh(incident)
        return incident

    def delete(self, db: Session, id: UUID):
        incident = db.get(Incident, id)

        if not incident:
            return False

        db.delete(incident)
        db.commit()
        return True

    def get_recent(self, db: Session, limit: int = 50):
        stmt = (
            select(Incident)
            .order_by(Incident.occurred_at.desc())
            .limit(limit)
        )
        return db.scalars(stmt).all()

    def get_multi_endpoint(self, db: Session, endpoint_ids: List[UUID]):
        stmt = (
            select(Incident)
            .where(Incident.endpoint_id.in_(endpoint_ids))
            .order_by(Incident.occurred_at.desc())
        )
        return db.scalars(stmt).all()