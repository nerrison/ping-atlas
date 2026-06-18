import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    endpoint_id = Column(
        UUID(as_uuid=True),
        ForeignKey("endpoints.id"),
        nullable=False,
        index=True
    )

    endpoint_url = Column(String)

    incident_time = Column(DateTime)

    error_msg = Column(String, nullable=True)

    status = Column(String)

    last_status_code = Column(Integer)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    endpoint = relationship(
        "Endpoint",
        back_populates="incidents"
    )