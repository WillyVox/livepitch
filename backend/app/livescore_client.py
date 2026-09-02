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

    async def fetch_standings(self, league_id: int, season: int) -> list[dict]:
        """
        GET /standings?league=<id>&season=<year> — API-FOOTBALL returns
        one table per group/stage; we flatten the first (main) table.
        """
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                f"{self.base_url}/standings",
                headers=self.headers,
                params={"league": league_id, "season": season},
            )
            resp.raise_for_status()
            data = resp.json()
            response = data.get("response", [])
            if not response:
                return []
            table = response[0]["league"]["standings"][0]
            return [normalize_standing_row(row) for row in table]


# Map our internal league slugs (used in URLs and the frontend) to
# API-FOOTBALL's numeric league IDs. Extend this as you add leagues.
LEAGUE_ID_MAP = {
    "pl": 39,          # Premier League
    "laliga": 140,      # La Liga
    "seriea": 135,       # Serie A
    "bundesliga": 78,   # Bundesliga
    "ligue1": 61,        # Ligue 1
    "ucl": 2,             # Champions League
}


def normalize_standing_row(row: dict) -> dict:
    """Flatten an API-FOOTBALL standings row into the frontend's table shape."""
    all_stats = row["all"]
    return {
        "rank": row["rank"],
        "team": row["team"]["name"],
        "played": all_stats["played"],
        "win": all_stats["win"],
        "draw": all_stats["draw"],
        "loss": all_stats["lose"],
        "gf": all_stats["goals"]["for"],
        "ga": all_stats["goals"]["against"],
        "points": row["points"],
        # API-FOOTBALL gives form as a string like "WWDLW"
        "form": list(row.get("form") or ""),
    }


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