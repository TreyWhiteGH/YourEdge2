from fastapi import APIRouter

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("")
def list_teams() -> dict[str, list]:
    return {"teams": []}
