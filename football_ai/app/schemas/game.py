from pydantic import BaseModel


class GamePreviewResponse(BaseModel):
    game_id: int
    message: str
    next: list[str]
