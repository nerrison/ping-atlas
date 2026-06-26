from sqlalchemy.orm import Session
from app.schemas.group import GroupCreate, GroupUpdate
from app.repositories.group import GroupRepository
import re


def generate_slug(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    return slug

class GroupService:
    def __init__(self, repo: GroupRepository):
        self.repo = repo


    def list_groups(self):
        return self.repo.list()

    def get_group(self, group_id):
        return self.repo.get_by_id( group_id)

    def create_group(self, data: GroupCreate):
        existing = self.repo.get_by_slug(generate_slug(data.name))
        if existing:
            raise ValueError("Group already exists")

        if len(data.name) < 3:
            raise ValueError("Name too short")

        slug = generate_slug(data.name)

        return self.repo.create(data, slug)

    def update_group(self, group_id, data: GroupUpdate):
        return self.repo.put(data, group_id)

    def patch_group(self, group_id, data: GroupUpdate):
        return self.repo.patch(data, group_id)

    def delete_group(self, group_id):
        return self.repo.delete(group_id)