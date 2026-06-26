from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.repositories.group import GroupRepository
from app.services.group import GroupService
from app.schemas.summary import GroupSummary
from app.schemas.group import GroupCreate, GroupUpdate

router = APIRouter(prefix="/groups", tags=["groups"])


def get_group_repo(db:Session = Depends(get_db)):
    return GroupRepository(db)


def get_group_service(repo: GroupRepository = Depends(get_group_repo)):
    return GroupService(repo)


@router.get("", response_model=list[GroupSummary])
def list_groups(
    service: GroupService = Depends(get_group_service),
):
    return service.list_groups()


@router.get("/{group_id}")
def get_group(
    group_id: str,
    db: Session = Depends(get_db),
    service: GroupService = Depends(get_group_service),
):
    return service.get_group(group_id)


@router.post("")
def create_group(
    data: GroupCreate,
    service: GroupService = Depends(get_group_service),
):
    return service.create_group(data)


@router.put("/{group_id}")
def update_group(
    group_id: str,
    data: GroupUpdate,
    service: GroupService = Depends(get_group_service),
):
    return service.update_group( group_id, data)


@router.patch("/{group_id}")
def patch_group(
    group_id: str,
    data: GroupUpdate,
    service: GroupService = Depends(get_group_service),
):
    return service.patch_group(group_id, data)


@router.delete("/{group_id}")
def delete_group(
    group_id: str,
    service: GroupService = Depends(get_group_service),
):
    return service.delete_group(group_id)