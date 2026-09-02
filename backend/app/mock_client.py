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