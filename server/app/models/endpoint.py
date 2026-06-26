from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.group import Group
    from app.models.history import History
    from app.models.incident import Incident


class Endpoint(Base):
    __tablename__ = "endpoints"

    __table_args__ = (
        UniqueConstraint("group_id", "url"),
    )
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("groups.id"),
        nullable=False,
        index=True,
    )

    type: Mapped[str | None] = mapped_column(String)

    status: Mapped[str] = mapped_column(
        Enum("UP", "DOWN", "DEGRADED", name="endpoint_status"),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String,
        nullable=False,unique=True
    )

    description: Mapped[str | None] = mapped_column(String)

    method: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    response_time: Mapped[int | None] = mapped_column(Integer)
    last_check: Mapped[datetime | None] = mapped_column(DateTime)
    uptime: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    group: Mapped["Group"] = relationship(
        back_populates="endpoints",
    )

    histories: Mapped[list["History"]] = relationship(
        back_populates="endpoint",
        cascade="all, delete-orphan",
    )

    incidents: Mapped[list["Incident"]] = relationship(
        back_populates="endpoint",
        cascade="all, delete-orphan",
    )