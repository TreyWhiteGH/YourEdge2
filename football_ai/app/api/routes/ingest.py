from fastapi import APIRouter

from app.services.espn_client import ESPNClient

router = APIRouter(prefix="/ingest", tags=["ingest"])
client = ESPNClient()


@router.get("/{league}/scoreboard")
def ingest_scoreboard(league: str, dates: str | None = None):
    return client.get_scoreboard(league=league, dates=dates)


@router.get("/{league}/game/{event_id}")
def ingest_game_summary(league: str, event_id: str):
    return client.get_summary(league=league, event_id=event_id)


@router.get("/{league}/team/{team_id}/roster")
def ingest_team_roster(league: str, team_id: str):
    return client.get_team_roster(league=league, team_id=team_id)


@router.get("/{league}/team/{team_id}/injuries")
def ingest_team_injuries(league: str, team_id: str):
    return client.get_team_injuries(league=league, team_id=team_id)


@router.get("/{league}/news")
def ingest_news(league: str):
    return client.get_news(league=league)
