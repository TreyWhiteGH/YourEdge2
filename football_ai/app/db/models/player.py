from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), index=True)
    espn_athlete_id: Mapped[str | None] = mapped_column(String(32), unique=True)
    full_name: Mapped[str] = mapped_column(String(128), index=True)
    short_name: Mapped[str | None] = mapped_column(String(64))
    position: Mapped[str | None] = mapped_column(String(16), index=True)
    jersey: Mapped[str | None] = mapped_column(String(8))
    headshot_url: Mapped[str | None] = mapped_column(String(512))
    active: Mapped[bool] = mapped_column(default=True)
