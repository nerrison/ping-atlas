from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.deps import get_db
from app.repositories.history import HistoryRepository
from app.services.history import HistoryService

router = APIRouter(prefix="/histories", tags=["histories"])


def get_history_service(db: Session = Depends(get_db)):
    repo = HistoryRepository(db)
    return HistoryService(repo)


@router.get("")
def list_history(
    service: HistoryService = Depends(get_history_service),
):
    return service.list_history()


@router.get("/{history_id}")
def get_history(
    history_id: UUID,
    service: HistoryService = Depends(get_history_service),
):
    return service.get_history(history_id)


@router.get("/endpoint/{endpoint_id}/chart")
def endpoint_chart(
    endpoint_id: UUID,
    service: HistoryService = Depends(get_history_service),
):
    return service.get_endpoint_chart(endpoint_id)


#@router.post("/chart/multi")
#def multi_chart(
#    endpoint_ids: list[UUID],
#    service: HistoryService = Depends#(get_history_service),
#):
#    return service.get_multi_endpoint_chart#(endpoint_ids)
#