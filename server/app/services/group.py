from sqlalchemy.orm import Session
from app.schemas.group import GroupCreate, GroupResponse, GroupUpdate
from app.schemas.summary import GroupSummary
from app.repositories.group import GroupRepository
import re


def generate_slug(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"\s+", "-", slug)       # spaces → hyphens
    slug = re.sub(r"[^a-z0-9\-]", "", slug)  # remove invalid chars
    return slug

class GroupService:
    def __init__(self):
        self.repo = GroupRepository()

    def create_group(self, db, data: GroupCreate):

        slug = generate_slug(data.name)

        # ensure uniqueness
        if self.repo.get_by_slug(db, slug):
            raise ValueError("Group already exists")
        

        return self.repo.create(db, data, slug)
    
    def get_group(self, db, data:GroupSummary, id):
        pass

    def list_groups(self, db, data:GroupResponse, id):
        pass

    def update_group(self, db, data:GroupUpdate,id):
        pass

