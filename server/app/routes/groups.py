from fastapi import APIRouter,Depends
from app.schemas.group import GroupCreate
from app.models.group import Group
from app.db.database import engine, Base
from sqlalchemy.orm import Session
from app.db.deps import get_db

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("/")
def create_group(group: GroupCreate, db: Session = Depends(get_db)):

    new_group = Group(
        name=group.name,
        slug=group.slug,
        type=group.type,
        description=group.description
    )

    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    return new_group