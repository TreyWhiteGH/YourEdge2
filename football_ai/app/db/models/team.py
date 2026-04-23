from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    league_id: Mapped[int] = mapped_column(ForeignKey("leagues.id"), index=True)
    espn_team_id: Mapped[str | None] = mapped_column(String(32), unique=True)
    display_name: Mapped[str] = mapped_column(String(128), index=True)
    short_name: Mapped[str | None] = mapped_column(String(64))
    abbreviation: Mapped[str | None] = mapped_column(String(16), index=True)
    location: Mapped[str | None] = mapped_column(String(64))
    nickname: Mapped[str | None] = mapped_column(String(64))
    color: Mapped[str | None] = mapped_column(String(16))
    alternate_color: Mapped[str | None] = mapped_column(String(16))
    logo_url: Mapped[str | None] = mapped_column(String(512))
