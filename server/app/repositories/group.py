from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate, GroupPatch


class GroupRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_by_slug(self, slug: str):
        stmt = select(Group).where(Group.slug == slug)
        return self.db.scalars(stmt).first()

    def get_by_id(self, id: UUID):
        return self.db.get(Group, id)

    def list(self):
        return self.db.scalars(select(Group)).all()

    def create(self, data: GroupCreate, slug: str):
        group = Group(
            name=data.name,
            slug=slug,
            type=data.type,
            description=data.description,
        )

        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def put(self, data: GroupUpdate, id: UUID, slug:str):
        group = self.db.get(Group, id)
        if not group:
            return None

        group.name = data.name or group.name
        group.slug = slug or group.slug
        group.type = data.type
        group.description = data.description

        self.db.commit()
        self.db.refresh(group)
        return group

    def patch(self, data: GroupPatch, id: UUID, slug):
        group = self.db.get(Group, id)
        if not group:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(group, key, value)

        if slug is not None:
            group.slug = slug

        self.db.commit()
        self.db.refresh(group)
        return group

    def delete(self, id: UUID):
        group = self.db.get(Group, id)
        if not group:
            return False

        self.db.delete(group)
        self.db.commit()
        return True