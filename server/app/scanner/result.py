from dataclasses import dataclass
from uuid import UUID

from app.models.endpoint import EndpointStatus


@dataclass
class ScanResult:
    endpoint_id: UUID
    status: EndpointStatus
    status_code: int | None
    response_time: int | None
    message: str | None