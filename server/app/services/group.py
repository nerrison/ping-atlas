from sqlalchemy.orm import Session
from app.schemas.group import GroupCreate, GroupUpdate, GroupPatch
from app.repositories.group import GroupRepository
import re


def generate_slug(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    return slug

class GroupService:
    def __init__(self,db:Session, repo: GroupRepository):
        self.db = db
        self.repo = repo


    def list_groups(self):
        return self.repo.list()

    def get_group(self, group_id):
        if not group_id:
            raise ValueError("No group found")
        
        group = self.repo.get_by_id(group_id)

        if group is None:
            raise ValueError("Group not found")
        
        return group

    def create_group(self, data: GroupCreate):
        try:
            existing = self.repo.get_by_slug(generate_slug(data.name))
            if existing:
                raise ValueError("Group already exists")

            if len(data.name) < 3:
                raise ValueError("Name too short")

            slug = generate_slug(data.name)
            group = self.repo.create(data,slug)

            self.db.commit()
            self.db.refresh(group)

            return group
        except Exception:
            self.db.rollback()
            raise

    def update_group(self, group_id, data: GroupUpdate):
        try:
            slug = generate_slug(data.name)
            group = self.repo.put(data, group_id, slug)

            if group is None:
                raise ValueError("Group not found")

            self.db.commit()
            self.db.refresh(group)

            return group
        
        except Exception:
            self.db.rollback()
            raise

    def patch_group(self, group_id, data: GroupPatch):
        
        try:
            slug = None
        
            if data.name is not None:
                slug = generate_slug(data.name) 
            
            group = self.repo.patch(data, group_id, slug)

            if group is None:
                raise ValueError("Group not found")

            self.db.commit()
            self.db.refresh(group)

            return group
        
        except Exception:
            self.db.rollback()
            raise

    def delete_group(self, group_id):
        
        try:
            deleted = self.repo.delete(group_id)

            if not deleted:
                    raise ValueError("Group not found")

            self.db.commit()

            return True
        
        except Exception:
            self.db.rollback()
            raise