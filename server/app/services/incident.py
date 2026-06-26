from uuid import UUID
from app.repositories.incident import IncidentRepository
from app.utils.time import utc_now


class IncidentService:
    def __init__(self, repo: IncidentRepository):
        self.repo = repo

    def record_incident(
        self,
        endpoint_id: UUID,
        endpoint_url: str | None,
        status: str | None,
        status_code: int | None,
        error_message: str | None,
    ):
        return self.repo.create(
            endpoint_id=endpoint_id,
            endpoint_url=endpoint_url,
            status=status,
            status_code=status_code,
            error_message=error_message,
            occurred_at=utc_now(),
        )

    def get_by_endpoint(self, endpoint_id: UUID):
        return self.repo.get_by_endpoint(endpoint_id)
    
    def list_recent_incidents(self, limit: int = 50):
        return self.repo.get_recent(limit)

    def get_dashboard_incidents(self, endpoint_ids: list[UUID]):
        return self.repo.get_multi_endpoint(endpoint_ids)