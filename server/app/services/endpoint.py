from sqlalchemy.orm import Session
from app.schemas.endpoint import EndpointCreate, EndpointUpdate, EndpointPut
from app.repositories.endpoint import EndpointRepository


class EndpointService:
    def __init__(self, db: Session, repo: EndpointRepository):
        self.db = db
        self.repo = repo

    def list_endpoints_per_group(self, group_id):
        group = self.repo.get_group_by_id(group_id)

        if group is None:
            raise ValueError("Group not found")

        return self.repo.list(group_id)

    def get_endpoint(self, id):
        if not id:
            raise ValueError("No endpoint found")

        endpoint = self.repo.get(id)

        if endpoint is None:
            raise ValueError("Endpoint not found")

        return endpoint

    def list_endpoints(self):
        return self.repo.list_all()

    def create_endpoint(self, data: EndpointCreate, group_id):
        try:
            group = self.repo.get_group_by_id(group_id)

            if group is None:
                raise ValueError("Group not found")

            data.url = data.url.strip()

            existing = self.repo.get_by_url(data.url, group_id)

            if existing:
                raise ValueError("Endpoint already exists in this group")

            endpoint = self.repo.create(data, group_id)

            self.db.commit()
            self.db.refresh(endpoint)

            return endpoint

        except Exception:
            self.db.rollback()
            raise

    def update_endpoint(self, data: EndpointPut, id):
        try:
            endpoint = self.repo.get_by_id(id)

            if endpoint is None:
                raise ValueError("Endpoint not found")

            endpoint = self.repo.put(data, id)

            self.db.commit()
            self.db.refresh(endpoint)

            return endpoint

        except Exception:
            self.db.rollback()
            raise

    def patch_endpoint(self, data: EndpointUpdate, id):
        try:
            endpoint = self.repo.patch(data, id)

            if endpoint is None:
                raise ValueError("Endpoint not found")

            self.db.commit()
            self.db.refresh(endpoint)

            return endpoint

        except Exception:
            self.db.rollback()
            raise

    def delete_endpoint(self, id):
        try:
            deleted = self.repo.delete(id)

            if not deleted:
                raise ValueError("Endpoint not found")

            self.db.commit()

            return True

        except Exception:
            self.db.rollback()
            raise