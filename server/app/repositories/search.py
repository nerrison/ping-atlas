from sqlalchemy import select, or_
from app.models.group import Group
from app.models.endpoint import Endpoint


class SearchRepository:

    def search_all(self, db, query: str):
        group_stmt = (
            select(Group)
            .where(Group.name.ilike(f"%{query}%"))
        )

        endpoint_stmt = (
            select(Endpoint)
            .where(
                or_(
                    Endpoint.url.ilike(f"%{query}%"),
                    Endpoint.type.ilike(f"%{query}%"),
                )
            )
        )

        groups = db.scalars(group_stmt).all()
        endpoints = db.scalars(endpoint_stmt).all()

        return groups, endpoints