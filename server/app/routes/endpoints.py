from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.deps import get_db
from app.repositories.endpoint import EndpointRepository
from app.services.endpoint import EndpointService
from app.schemas.endpoint import EndpointCreate, EndpointUpdate

group_router = APIRouter(prefix="/groups/{group_id}/endpoints", tags=["endpoints"])


def get_endpoint_repo(db: Session = Depends(get_db)):
    return EndpointRepository(db)


def get_endpoint_service(repo: EndpointRepository = Depends(get_endpoint_repo)):
    return EndpointService(repo)


@group_router.post("")
def create_endpoint(
    group_id: UUID,
    payload: EndpointCreate,
    service: EndpointService = Depends(get_endpoint_service),
):
    try:
        return service.create_endpoint(payload, group_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@group_router.get("")
def list_endpoints(
    group_id: UUID,
    service: EndpointService = Depends(get_endpoint_service),
):
    return service.list_endpoints_per_group(group_id)


@group_router.get("/{endpoint_id}")
def get_endpoint(
    group_id: UUID,
    endpoint_id: UUID,
    service: EndpointService = Depends(get_endpoint_service),
):
    result = service.get_endpoint(group_id, endpoint_id)

    if not result:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    return result


@group_router.put("/{endpoint_id}")
def update_endpoint(
    group_id: UUID,
    endpoint_id: UUID,
    payload: EndpointUpdate,
    service: EndpointService = Depends(get_endpoint_service),
):
    result = service.update_endpoint(payload, endpoint_id)

    if not result:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    return result


@group_router.patch("/{endpoint_id}")
def patch_endpoint(
    group_id: UUID,
    endpoint_id: UUID,
    payload: EndpointUpdate,
    service: EndpointService = Depends(get_endpoint_service),
):
    result = service.patch_endpoint(payload, endpoint_id)

    if not result:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    return result


@group_router.delete("/{endpoint_id}")
def delete_endpoint(
    endpoint_id: UUID,
    service: EndpointService = Depends(get_endpoint_service),
):
    ok = service.delete_endpoint(endpoint_id)

    if not ok:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    return {"message": "Endpoint deleted"}


endpoint_router = APIRouter(prefix="/endpoints", tags=["endpoints"])

@endpoint_router.get("")
def list_all_endpoints(service:EndpointService=Depends(get_endpoint_service)):
    return service.list_endpoints()