"""
Adapter around the live-score data provider.

Default implementation targets API-FOOTBALL (api-sports.io / RapidAPI),
a widely-used commercial football data API with:
  - /fixtures?live=all              -> all matches currently in play
  - /fixtures?id=<id>                -> single fixture with events, lineups
  - /fixtures/lineups?fixture=<id>   -> starting XI + formation
  - /leagues                         -> league metadata

Docs: https://www.api-football.com/documentation-v3

If you buy a different provider (LiveScore API on RapidAPI, SportMonks,
Sportradar, etc.), implement the same three methods
(fetch_live_fixtures / fetch_lineups / normalize) against their schema —
everything downstream (event detection, websocket broadcast, frontend)
only depends on the normalized shape defined in `normalize_fixture`.
"""
from __future__ import annotations

import httpx

from app.config import settings
from app.mock_client import MockClient


class ApiFootballClient:
    def __init__(self) -> None:
        self.base_url = settings.API_FOOTBALL_BASE_URL
        self.headers = {"x-apisports-key": settings.API_FOOTBALL_KEY}

    async def fetch_live_fixtures(self) -> list[dict]:
        """Pull every fixture currently in play, across all leagues."""
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                f"{self.base_url}/fixtures",
                headers=self.headers,
                params={"live": "all"},
            )
            resp.raise_for_status()
            data = resp.json()
            return [normalize_fixture(f) for f in data.get("response", [])]

    async def fetch_lineups(self, fixture_id: int) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                f"{self.base_url}/fixtures/lineups",
                headers=self.headers,
                params={"fixture": fixture_id},
            )
            resp.raise_for_status()
            return resp.json().get("response", [])


def normalize_fixture(raw: dict) -> dict:
    """
    Convert an API-FOOTBALL fixture object into the flat shape the
    frontend expects (see frontend/src/data/mockData.js for the schema).
    """
    fixture = raw["fixture"]
    league = raw["league"]
    teams = raw["teams"]
    goals = raw["goals"]

    status_map = {
        "1H": "LIVE", "2H": "LIVE", "ET": "LIVE", "P": "LIVE", "LIVE": "LIVE",
        "HT": "HT",
        "FT": "FT", "AET": "FT", "PEN": "FT",
        "NS": "UPCOMING",
    }
    short_status = fixture["status"]["short"]

    events = [
        {
            "minute": e["time"]["elapsed"],
            "type": _event_type(e),
            "team": "home" if e["team"]["id"] == teams["home"]["id"] else "away",
            "player": e.get("player", {}).get("name") or "Unknown",
        }
        for e in raw.get("events", [])
        if _event_type(e) is not None
    ]

    return {
        "id": str(fixture["id"]),
        "league": league["name"],
        "status": status_map.get(short_status, short_status),
        "minute": fixture["status"]["elapsed"] or 0,
        "kickoff": fixture["date"][11:16],
        "home": {"name": teams["home"]["name"], "score": goals["home"], "logo": teams["home"]["logo"]},
        "away": {"name": teams["away"]["name"], "score": goals["away"], "logo": teams["away"]["logo"]},
        "events": events,
    }


def _event_type(e: dict) -> str | None:
    kind = e.get("type", "").lower()
    detail = e.get("detail", "").lower()
    if kind == "goal":
        return "goal"
    if kind == "card" and "yellow" in detail:
        return "yellow"
    if kind == "card" and "red" in detail:
        return "red"
    return None


def get_client() -> ApiFootballClient | MockClient:
    # Swap this for another provider's client if needed.
    if settings.USE_MOCK_DATA:
        return MockClient()
    return ApiFootballClient()

