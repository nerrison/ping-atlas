from sqlalchemy.orm import Session
from app.models.group import Group
from app.schemas.group import GroupCreate


class GroupRepository:
    def get_by_slug(self, db: Session, slug: str):
        return db.query(Group).filter(Group.slug == slug).first()
    
    def create(self, db, data: GroupCreate, slug: str):
        group = Group(
            name=data.name,
            slug=slug,
            type=data.type,
            description=data.description
        )

        db.add(group)
        db.commit()
        db.refresh(group)
        return group