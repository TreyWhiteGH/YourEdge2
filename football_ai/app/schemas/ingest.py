from pydantic import BaseModel


class IngestResponse(BaseModel):
    detail: str
