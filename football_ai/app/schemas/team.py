from pydantic import BaseModel


class TeamResponse(BaseModel):
    id: int
    display_name: str
