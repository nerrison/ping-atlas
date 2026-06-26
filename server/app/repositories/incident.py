from uuid import UUID
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from app.models.incident import Incident


class IncidentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        endpoint_id: UUID,
        endpoint_url: str | None,
        status: str | None,
        status_code: int | None,
        error_message: str | None,
        occurred_at: datetime,
    ):
        incident = Incident(
            endpoint_id=endpoint_id,
            endpoint_url=endpoint_url,
            status=status,
            status_code=status_code,
            error_message=error_message,
            occurred_at=occurred_at,
        )

        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def get_by_id(self, id: UUID):
        return self.db.get(Incident, id)

    def get_by_endpoint(self, endpoint_id: UUID):
        return self.db.scalars(
            select(Incident)
            .where(Incident.endpoint_id == endpoint_id)
            .order_by(Incident.occurred_at.desc())
        ).all()

    def list(self):
        return self.db.scalars(select(Incident)).all()

    def get_recent(self, limit: int = 50):
        return self.db.scalars(
            select(Incident)
            .order_by(Incident.occurred_at.desc())
            .limit(limit)
        ).all()

    def get_multi_endpoint(self, endpoint_ids: List[UUID]):
        return self.db.scalars(
            select(Incident)
            .where(Incident.endpoint_id.in_(endpoint_ids))
            .order_by(Incident.occurred_at.desc())
        ).all()