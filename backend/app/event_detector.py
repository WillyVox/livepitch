"""
Compares the previous polled snapshot of a fixture against the new one
and returns any *newly appeared* events (goal / yellow / red). This is
what triggers both the WebSocket "update" push and the social auto-post.
"""
from __future__ import annotations


def diff_events(previous: dict | None, current: dict) -> list[dict]:
    if previous is None:
        return []  # first time we see this fixture — nothing to diff yet

    prev_keys = {_event_key(e) for e in previous.get("events", [])}
    new_events = [e for e in current.get("events", []) if _event_key(e) not in prev_keys]
    return new_events


def _event_key(e: dict) -> tuple:
    return (e["minute"], e["type"], e["team"], e["player"])
