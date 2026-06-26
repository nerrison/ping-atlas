from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.endpoint import Endpoint


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    endpoint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("endpoints.id"),
        nullable=False,
        index=True,
    )

    endpoint_url: Mapped[str | None] = mapped_column(String)

    occurred_at: Mapped[datetime | None] = mapped_column(DateTime)

    error_message: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    status: Mapped[str | None] = mapped_column(String)

    status_code: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    endpoint: Mapped["Endpoint"] = relationship(
        back_populates="incidents",
    )