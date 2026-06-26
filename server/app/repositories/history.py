from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from app.models.history import History
from app.schemas.history import MetricPoint


class HistoryRepository:

    def get_by_id(self, db: Session, id: UUID):
        return db.get(History, id)

    def get_by_endpoint(self, db: Session, endpoint_id: UUID):
        stmt = select(History).where(History.endpoint_id == endpoint_id)
        return db.scalars(stmt).all()

    def list(self, db: Session):
        return db.scalars(select(History)).all()

    def create(self, db: Session, data):
        history = History(
            endpoint_id=data.endpoint_id,
            latency=data.latency,
            availability=data.availability,
            error=data.error,
            check_time=data.timestamp,  # adjust if your schema uses timestamp
        )

        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    def delete(self, db: Session, id: UUID):
        history = db.get(History, id)
        if not history:
            return False

        db.delete(history)
        db.commit()
        return True

    def get_endpoint_chart(self, db: Session, endpoint_id: UUID):
        stmt = (
            select(History)
            .where(History.endpoint_id == endpoint_id)
            .order_by(History.check_time.asc())
        )

        histories = db.scalars(stmt).all()

        return [
            MetricPoint(
                check_time=h.check_time,
                latency=h.latency,
                availability=h.availability,
                errors=h.error,
            )
            for h in histories
        ]

    def get_multi_endpoint_chart(self, db: Session, endpoint_ids: List[UUID]):
        stmt = (
        select(History)
        .where(History.endpoint_id.in_(endpoint_ids))
        .order_by(History.check_time.asc())
    )

        histories = db.scalars(stmt).all()

        grouped: dict[UUID, list[MetricPoint]] = {}

        for h in histories:
            grouped.setdefault(h.endpoint_id, []).append(
                MetricPoint(
                    check_time=h.check_time,
                    latency=h.latency,
                    availability=h.availability,
                    errors=h.error,
                )
            )

        return grouped