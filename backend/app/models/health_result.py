from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class HealthResult(Base):
    __tablename__ = "health_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_name: Mapped[str] = mapped_column(String(120), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    ok: Mapped[bool] = mapped_column(Boolean, default=False)
    status_text: Mapped[str] = mapped_column(String(60), default="unknown")
    elasticsearch: Mapped[str] = mapped_column(String(40), default="unknown")
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
