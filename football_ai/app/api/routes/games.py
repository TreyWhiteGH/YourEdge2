from fastapi import APIRouter

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/{game_id}/preview")
def game_preview(game_id: int):
    return {
        "game_id": game_id,
        "message": "stub preview endpoint",
        "next": [
            "load game from postgres",
            "attach injuries/news",
            "compute simple recent-form preview",
        ],
    }
