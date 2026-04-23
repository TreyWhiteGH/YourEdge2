from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GamePlay(Base):
    __tablename__ = "game_plays"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
    drive_id: Mapped[int | None] = mapped_column(ForeignKey("game_drives.id"), index=True)
    play_index: Mapped[int] = mapped_column(Integer, index=True)
    raw_payload: Mapped[dict] = mapped_column(JSONB)
