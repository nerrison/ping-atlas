from uuid import UUID
from sqlalchemy import select
from typing import List
from sqlalchemy.orm import Session

from app.models.history import History
from app.schemas.history import MetricPoint
from app.mapper.history import to_metric_point


class HistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: UUID):
        return self.db.get(History, id)

    def get_by_endpoint(self, endpoint_id: UUID):
        stmt = select(History).where(History.endpoint_id == endpoint_id)
        return self.db.scalars(stmt).all()

    def list(self):
        return self.db.scalars(select(History)).all()

    def create(self, data):
        history = History(
            endpoint_id=data.endpoint_id,
            latency=data.latency,
            availability=data.availability,
            error=data.error,
            check_time=data.timestamp,
        )

        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history



    def get_endpoint_chart(self, endpoint_id: UUID):
        stmt = (
            select(History)
            .where(History.endpoint_id == endpoint_id)
            .order_by(History.check_time.asc())
        )

        histories = self.db.scalars(stmt).all()

        return [to_metric_point(h) for h in histories]

    def get_multi_endpoint(self, endpoint_ids: List[UUID]):
        stmt = (
            select(History)
            .where(History.endpoint_id.in_(endpoint_ids))
            .order_by(History.check_time.asc())
        )

        histories = self.db.scalars(stmt).all()

        grouped: dict[UUID, list[MetricPoint]] = {}

        for h in histories:
            grouped.setdefault(h.endpoint_id, []).append(to_metric_point(h))

        return grouped