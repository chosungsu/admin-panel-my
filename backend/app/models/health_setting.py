from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class HealthSetting(Base):
    __tablename__ = "health_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    polling_interval_ms: Mapped[int] = mapped_column(Integer, default=5000)
    auto_refresh: Mapped[bool] = mapped_column(Boolean, default=True)
    max_points: Mapped[int] = mapped_column(Integer, default=90)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
