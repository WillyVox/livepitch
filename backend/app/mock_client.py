from __future__ import annotations

import copy
import random


class MockClient:
    def __init__(self) -> None:
        self.matches = [
            {
                "id": "1001",
                "league": "Premier League",
                "status": "LIVE",
                "minute": 23,
                "kickoff": "20:00",
                "home": {
                    "name": "Arsenal",
                    "score": 0,
                    "logo": "https://media.api-sports.io/football/teams/42.png",
                },
                "away": {
                    "name": "Chelsea",
                    "score": 0,
                    "logo": "https://media.api-sports.io/football/teams/49.png",
                },
                "events": [],
                "home_scorers": ["B. Saka", "G. Martinelli", "M. Ødegaard"],
                "away_scorers": ["C. Palmer", "N. Jackson", "E. Fernández"],
            },
            {
                "id": "1002",
                "league": "Premier League",
                "status": "LIVE",
                "minute": 67,
                "kickoff": "19:30",
                "home": {
                    "name": "Manchester City",
                    "score": 1,
                    "logo": "https://media.api-sports.io/football/teams/50.png",
                },
                "away": {
                    "name": "Liverpool",
                    "score": 1,
                    "logo": "https://media.api-sports.io/football/teams/40.png",
                },
                "events": [
                    {"minute": 12, "type": "goal", "team": "home", "player": "E. Haaland"},
                    {"minute": 44, "type": "goal", "team": "away", "player": "M. Salah"},
                ],
                "home_scorers": ["E. Haaland", "K. De Bruyne", "P. Foden"],
                "away_scorers": ["M. Salah", "L. Díaz", "C. Gakpo"],
            },
            {
                "id": "1003",
                "league": "La Liga",
                "status": "HT",
                "minute": 45,
                "kickoff": "20:15",
                "home": {
                    "name": "Real Madrid",
                    "score": 2,
                    "logo": "https://media.api-sports.io/football/teams/541.png",
                },
                "away": {
                    "name": "Barcelona",
                    "score": 0,
                    "logo": "https://media.api-sports.io/football/teams/529.png",
                },
                "events": [
                    {"minute": 18, "type": "goal", "team": "home", "player": "Vini Jr."},
                    {"minute": 35, "type": "goal", "team": "home", "player": "J. Bellingham"},
                    {"minute": 41, "type": "yellow", "team": "away", "player": "Gavi"},
                ],
                "home_scorers": ["Vini Jr.", "J. Bellingham", "K. Mbappé"],
                "away_scorers": ["R. Lewandowski", "L. Yamal"],
            },
            {
                "id": "1004",
                "league": "Serie A",
                "status": "LIVE",
                "minute": 82,
                "kickoff": "18:45",
                "home": {
                    "name": "Inter",
                    "score": 0,
                    "logo": "https://media.api-sports.io/football/teams/505.png",
                },
                "away": {
                    "name": "AC Milan",
                    "score": 1,
                    "logo": "https://media.api-sports.io/football/teams/489.png",
                },
                "events": [
                    {"minute": 55, "type": "goal", "team": "away", "player": "R. Leão"},
                    {"minute": 72, "type": "yellow", "team": "home", "player": "N. Barella"},
                ],
                "home_scorers": ["L. Martínez", "M. Thuram"],
                "away_scorers": ["R. Leão", "C. Pulisic"],
            },
        ]

    async def fetch_live_fixtures(self) -> list[dict]:
        """Simulate real-time progression across multiple live matches."""
        for match in self.matches:
            # Skip progression for halftime or finished matches
            if match["status"] != "LIVE":
                continue

            match["minute"] += 1
            if match["minute"] >= 90:
                match["status"] = "FT"
                continue

            # Random event generation
            roll = random.random()
            if roll < 0.12:
                # Home Goal
                match["home"]["score"] += 1
                match["events"].append(
                    {
                        "minute": match["minute"],
                        "type": "goal",
                        "team": "home",
                        "player": random.choice(match["home_scorers"]),
                    }
                )
            elif roll < 0.22:
                # Away Goal
                match["away"]["score"] += 1
                match["events"].append(
                    {
                        "minute": match["minute"],
                        "type": "goal",
                        "team": "away",
                        "player": random.choice(match["away_scorers"]),
                    }
                )
            elif roll < 0.32:
                # Yellow Card
                match["events"].append(
                    {
                        "minute": match["minute"],
                        "type": "yellow",
                        "team": random.choice(["home", "away"]),
                        "player": "Defensive Player",
                    }
                )
            elif roll < 0.35:
                # Red Card
                match["events"].append(
                    {
                        "minute": match["minute"],
                        "type": "red",
                        "team": random.choice(["home", "away"]),
                        "player": "Aggressive Player",
                    }
                )

        # Return sanitized copies without the temporary internal helper lists
        cleaned_matches = []
        for m in self.matches:
            m_copy = copy.deepcopy(m)
            m_copy.pop("home_scorers", None)
            m_copy.pop("away_scorers", None)
            cleaned_matches.append(m_copy)

        return cleaned_matches

    async def fetch_lineups(self, fixture_id: int) -> dict:
        return {}

    async def fetch_standings(self, league_id: int, season: int) -> list[dict]:
        """
        Mirrors ApiFootballClient.fetch_standings' signature and return
        shape (same as normalize_standing_row's output), so main.py's
        get_standings endpoint doesn't need to know or care whether it's
        talking to the real API or this mock.

        league_id here is the *numeric* API-FOOTBALL id, since main.py
        looks it up via LEAGUE_ID_MAP before calling this (e.g. 39 for
        Premier League) — so the mock lines up 1:1 with the real
        provider and USE_MOCK_DATA can be flipped without touching the
        frontend at all.
        """
        return copy.deepcopy(MOCK_STANDINGS.get(league_id, []))


# Keyed by API-FOOTBALL's numeric league id — see LEAGUE_ID_MAP in
# livescore_client.py. Extend alongside that map as you add leagues.
MOCK_STANDINGS = {
    39: [  # Premier League
        {"rank": 1, "team": "Arsenal", "played": 20, "win": 15, "draw": 3, "loss": 2, "gf": 42, "ga": 15, "points": 48, "form": ["W", "W", "D", "W", "W"]},
        {"rank": 2, "team": "Liverpool", "played": 20, "win": 14, "draw": 4, "loss": 2, "gf": 39, "ga": 18, "points": 46, "form": ["W", "D", "W", "W", "L"]},
        {"rank": 3, "team": "Manchester City", "played": 20, "win": 13, "draw": 5, "loss": 2, "gf": 44, "ga": 20, "points": 44, "form": ["D", "W", "W", "W", "D"]},
        {"rank": 4, "team": "Chelsea", "played": 20, "win": 12, "draw": 4, "loss": 4, "gf": 36, "ga": 22, "points": 40, "form": ["W", "L", "W", "D", "W"]},
        {"rank": 5, "team": "Aston Villa", "played": 20, "win": 11, "draw": 5, "loss": 4, "gf": 33, "ga": 24, "points": 38, "form": ["D", "W", "W", "L", "W"]},
        {"rank": 6, "team": "Tottenham", "played": 20, "win": 10, "draw": 5, "loss": 5, "gf": 34, "ga": 27, "points": 35, "form": ["L", "W", "D", "W", "W"]},
        {"rank": 7, "team": "Newcastle", "played": 20, "win": 9, "draw": 6, "loss": 5, "gf": 31, "ga": 26, "points": 33, "form": ["W", "D", "D", "L", "W"]},
        {"rank": 8, "team": "Manchester United", "played": 20, "win": 9, "draw": 4, "loss": 7, "gf": 27, "ga": 25, "points": 31, "form": ["L", "W", "L", "D", "W"]},
    ],
    140: [  # La Liga
        {"rank": 1, "team": "Real Madrid", "played": 20, "win": 16, "draw": 2, "loss": 2, "gf": 45, "ga": 16, "points": 50, "form": ["W", "W", "W", "D", "W"]},
        {"rank": 2, "team": "Barcelona", "played": 20, "win": 14, "draw": 3, "loss": 3, "gf": 43, "ga": 20, "points": 45, "form": ["W", "D", "W", "W", "L"]},
        {"rank": 3, "team": "Girona", "played": 20, "win": 13, "draw": 4, "loss": 3, "gf": 38, "ga": 22, "points": 43, "form": ["D", "W", "W", "D", "W"]},
        {"rank": 4, "team": "Atletico Madrid", "played": 20, "win": 12, "draw": 4, "loss": 4, "gf": 34, "ga": 21, "points": 40, "form": ["W", "L", "W", "W", "D"]},
    ],
    135: [  # Serie A
        {"rank": 1, "team": "Inter", "played": 20, "win": 16, "draw": 3, "loss": 1, "gf": 44, "ga": 12, "points": 51, "form": ["W", "W", "W", "W", "D"]},
        {"rank": 2, "team": "Juventus", "played": 20, "win": 13, "draw": 5, "loss": 2, "gf": 32, "ga": 15, "points": 44, "form": ["D", "W", "D", "W", "W"]},
        {"rank": 3, "team": "AC Milan", "played": 20, "win": 12, "draw": 4, "loss": 4, "gf": 35, "ga": 22, "points": 40, "form": ["W", "W", "L", "D", "W"]},
        {"rank": 4, "team": "Como", "played": 20, "win": 12, "draw": 4, "loss": 4, "gf": 35, "ga": 22, "points": 40, "form": ["W", "W", "L", "D", "W"]},
    ],
    78: [  # Bundesliga
        {"rank": 1, "team": "Bayer Leverkusen", "played": 18, "win": 15, "draw": 3, "loss": 0, "gf": 46, "ga": 14, "points": 48, "form": ["W", "W", "D", "W", "W"]},
        {"rank": 2, "team": "Bayern Munich", "played": 18, "win": 13, "draw": 2, "loss": 3, "gf": 48, "ga": 20, "points": 41, "form": ["W", "L", "W", "W", "D"]},
        {"rank": 3, "team": "Dortmund", "played": 18, "win": 10, "draw": 4, "loss": 4, "gf": 33, "ga": 24, "points": 34, "form": ["D", "W", "L", "W", "W"]},
    ],
    61: [  # Ligue 1
        {"rank": 1, "team": "PSG", "played": 19, "win": 15, "draw": 3, "loss": 1, "gf": 47, "ga": 15, "points": 48, "form": ["W", "W", "W", "D", "W"]},
        {"rank": 2, "team": "Monaco", "played": 19, "win": 11, "draw": 5, "loss": 3, "gf": 36, "ga": 24, "points": 38, "form": ["D", "W", "W", "L", "W"]},
        {"rank": 3, "team": "Marseille", "played": 19, "win": 10, "draw": 6, "loss": 3, "gf": 30, "ga": 20, "points": 36, "form": ["W", "D", "D", "W", "L"]},
    ],
    2: [  # Champions League
        {"rank": 1, "team": "Manchester City", "played": 6, "win": 5, "draw": 1, "loss": 0, "gf": 18, "ga": 5, "points": 16, "form": ["W", "W", "D", "W", "W"]},
        {"rank": 2, "team": "Real Madrid", "played": 6, "win": 4, "draw": 2, "loss": 0, "gf": 15, "ga": 6, "points": 14, "form": ["D", "W", "W", "D", "W"]},
        {"rank": 3, "team": "Bayern Munich", "played": 6, "win": 4, "draw": 1, "loss": 1, "gf": 17, "ga": 8, "points": 13, "form": ["W", "W", "L", "W", "D"]},
    ],
}