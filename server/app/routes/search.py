from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.repositories.search import SearchRepository
from app.services.search import SearchService

router = APIRouter(prefix="/search", tags=["search"])

def get_search_repo():
    return SearchRepository()


def get_search_service(
    repo: SearchRepository = Depends(get_search_repo),
):
    return SearchService(repo)

@router.get("")
def search(
    q: str = Query(default =""),
    db: Session = Depends(get_db),
    service: SearchService = Depends(get_search_service),
):
    return service.search(db, q)