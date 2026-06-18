import uuid
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.database import Base


class History(Base):
    __tablename__ = "histories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    endpoint_id = Column(
        UUID(as_uuid=True),
        ForeignKey("endpoints.id"),
        nullable=False,
        index=True
    )

    latency = Column(Integer)
    availability = Column(Integer)
    error = Column(Integer)
    check_time = Column(DateTime)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    endpoint = relationship(
        "Endpoint",
        back_populates="histories"
    )