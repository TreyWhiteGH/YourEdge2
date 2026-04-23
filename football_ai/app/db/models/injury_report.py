from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class InjuryReport(Base):
    __tablename__ = "injury_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)
    player_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"), index=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    status: Mapped[str | None] = mapped_column(String(32), index=True)
    detail: Mapped[str | None] = mapped_column(String(256))
    raw_payload: Mapped[dict] = mapped_column(JSONB)
