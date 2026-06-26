from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.endpoint import Endpoint


class History(Base):
    __tablename__ = "histories"

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

    latency: Mapped[int] = mapped_column(Integer, nullable=False)

    availability: Mapped[float] = mapped_column(nullable=False)

    error: Mapped[int] = mapped_column(Integer, nullable=False)
    
    check_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    endpoint: Mapped["Endpoint"] = relationship(
        back_populates="histories",
    )