import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
    func
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base


class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey("groups.id"),
        nullable=False,
        index=True
    )

    type = Column(String)

    status = Column(
        Enum("UP", "DOWN", "DEGRADED", name="endpoint_status"),
        nullable=False
    )

    url = Column(String, nullable=False)
    description = Column(String)
    method = Column(String, nullable=False)

    response_time = Column(Integer)
    last_check = Column(DateTime)
    uptime = Column(Integer)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    group = relationship(
        "Group",
        back_populates="endpoints"
    )

    histories = relationship(
        "History",
        back_populates="endpoint",
        cascade="all, delete-orphan"
    )

    incidents = relationship(
        "Incident",
        back_populates="endpoint",
        cascade="all, delete-orphan"
    )