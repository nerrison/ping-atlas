from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate


class GroupRepository:

    def get_by_slug(self, db: Session, slug: str):
        stmt = select(Group).where(Group.slug == slug)
        return db.scalars(stmt).first()

    def get_by_id(self, db: Session, id: UUID):
        return db.get(Group, id)

    def list(self, db: Session):
        return db.scalars(select(Group)).all()

    def create(self, db: Session, data: GroupCreate, slug: str):
        group = Group(
            name=data.name,
            slug=slug,
            type=data.type,
            description=data.description,
        )

        db.add(group)
        db.commit()
        db.refresh(group)
        return group

    def put(self, db: Session, data: GroupUpdate, id: UUID):
        group = db.get(Group, id)
        if not group:
            return None

        group.name = data.name or group.name
        group.slug = data.slug or group.slug
        group.type = data.type
        group.description = data.description

        db.commit()
        db.refresh(group)
        return group

    def patch(self, db: Session, data: GroupUpdate, id: UUID):
        group = db.get(Group, id)
        if not group:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(group, key, value)

        db.commit()
        db.refresh(group)
        return group

    def delete(self, db: Session, id: UUID):
        group = db.get(Group, id)
        if not group:
            return False

        db.delete(group)
        db.commit()
        return True