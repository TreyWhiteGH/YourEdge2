from typing import Any

import httpx

from app.core.config import settings


class ESPNClient:
    def __init__(self) -> None:
        self.base_url = settings.espn_base_url
        self.cdn_base_url = settings.espn_cdn_base_url
        self.client = httpx.Client(timeout=20.0)

    def get_json(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_scoreboard(self, league: str, group: int | None = None, dates: str | None = None) -> dict[str, Any]:
        url = f"{self.base_url}/football/{league}/scoreboard"
        params: dict[str, Any] = {}
        if group is not None:
            params["groups"] = group
        if dates is not None:
            params["dates"] = dates
        return self.get_json(url, params)

    def get_summary(self, league: str, event_id: str) -> dict[str, Any]:
        url = f"{self.base_url}/football/{league}/summary"
        return self.get_json(url, {"event": event_id})

    def get_team_roster(self, league: str, team_id: str) -> dict[str, Any]:
        url = f"{self.base_url}/football/{league}/teams/{team_id}/roster"
        return self.get_json(url)

    def get_team_injuries(self, league: str, team_id: str) -> dict[str, Any]:
        url = f"{self.base_url}/football/{league}/teams/{team_id}/injuries"
        return self.get_json(url)

    def get_news(self, league: str) -> dict[str, Any]:
        url = f"{self.base_url}/football/{league}/news"
        return self.get_json(url)

    def get_team_news(self, league: str, team_id: str) -> dict[str, Any]:
        url = f"{self.base_url}/football/{league}/teams/{team_id}/news"
        return self.get_json(url)

    def close(self) -> None:
        self.client.close()
