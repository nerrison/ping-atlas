from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.group import GroupCreate, GroupResponse
from app.services.group import GroupService

router = APIRouter(prefix="/groups", tags=["groups"])

service = GroupService()


@router.post("/", response_model=GroupResponse)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    return service.create_group(db, group)