from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RosterSnapshot(Base):
    __tablename__ = "roster_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    raw_payload: Mapped[dict] = mapped_column(JSONB)
    depth_position: Mapped[str | None] = mapped_column(String(16))
    status: Mapped[str | None] = mapped_column(String(32))
