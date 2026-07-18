from uuid import UUID
from typing import List, Dict
from sqlalchemy.orm import Session
from app.repositories.history import HistoryRepository
from app.schemas.history import MetricPoint


class HistoryService:
    def __init__(self,db:Session, repo: HistoryRepository):
        self.db = db
        self.repo = repo

    def get_history(self, id: UUID):
        if not id:
            raise ValueError ("No history found")
        
        history = self.repo.get_by_id(id)

        if history is None:
            raise ValueError (" No history found")
        
        return history

    def list_history(self):
        return self.repo.list()


    def create_history(self, data):
        try:
            if not data:
                raise ValueError ("No data")
            
            history = self.repo.create(data)

            self.db.commit()
            self.db.refresh(history)

            return history
        except Exception:
            self.db.rollback()
            raise


    def get_endpoint_chart(self, endpoint_id: UUID) -> list[MetricPoint]:
        if not endpoint_id:
            raise ValueError ("No endpoint found")
        
        histories = self.repo.get_by_endpoint(endpoint_id)
        
        return [
            MetricPoint(
                check_time=h.check_time,
                latency=h.latency,
                availability=h.availability,
                error=h.error,
            )
            for h in histories
        ]


    def get_multi_endpoint_chart(self, endpoint_ids: list[UUID]):

        if not endpoint_ids:
             raise ValueError ("No endpoints found")
         
        histories = self.repo.get_multi_endpoint(endpoint_ids)

        grouped: dict[UUID, list[MetricPoint]] = {}

        for endpoint_id, items in histories.items():
            grouped[endpoint_id] = [
                MetricPoint(
                    check_time=h.check_time,
                    latency=h.latency,
                    availability=h.availability,
                    error=h.error,
                )
                for h in items
            ]

        return grouped