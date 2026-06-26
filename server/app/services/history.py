from uuid import UUID
from typing import List, Dict

from app.repositories.history import HistoryRepository
from app.schemas.history import MetricPoint


class HistoryService:
    def __init__(self, repo: HistoryRepository):
        self.repo = repo

    def get_history(self, id: UUID):
        return self.repo.get_by_id(id)

    def list_history(self):
        return self.repo.list()


    def create_history(self, data):
        return self.repo.create(data)


    def get_endpoint_chart(self, endpoint_id: UUID) -> list[MetricPoint]:
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