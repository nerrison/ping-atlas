from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.repositories.incident import IncidentRepository
from app.services.incident import IncidentService


router = APIRouter(prefix="/incidents", tags=["incidents"])


def get_incident_repo(db: Session = Depends(get_db)):
    return IncidentRepository(db)


def get_incident_service(
    repo: IncidentRepository = Depends(get_incident_repo),
):
    return IncidentService(repo)


@router.get("/recent")
def get_recent_incidents(
    limit: int = 50,
    service: IncidentService = Depends(get_incident_service),
):
    return service.list_recent_incidents(limit)


@router.get("/endpoint/{endpoint_id}")
def get_by_endpoint(
    endpoint_id: UUID,
    service: IncidentService = Depends(get_incident_service),
):
    return service.get_by_endpoint(endpoint_id)


@router.get("/dashboard")
def get_dashboard_incidents(
    endpoint_ids: list[UUID],
    service: IncidentService = Depends(get_incident_service),
):
    return service.get_dashboard_incidents(endpoint_ids)