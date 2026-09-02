# LivePitch — Backend

FastAPI service that polls a live football-data API, detects new events
(goals/cards), and pushes updates to the frontend over WebSocket while
optionally auto-posting to social media.

## How it works, step by step

**1. Choose and buy a data provider.**
This project defaults to **API-FOOTBALL** (api-sports.io, also listed on
RapidAPI as "API-FOOTBALL"), because it has a clean REST schema, a free
tier for testing, and paid tiers with short polling intervals for
near-real-time data. Plans: https://www.api-football.com/pricing
Alternatives with similar shapes: LiveScore API (RapidAPI), SportMonks,
Sportradar (enterprise-grade, pricier, true push websockets on top
tiers). The adapter pattern in `app/livescore_client.py` means swapping
providers later only touches one file.

**2. Get your API key and put it in `.env`.**
```bash
cp .env.example .env
# edit .env, set API_FOOTBALL_KEY=xxxxx
```

**3. `app/livescore_client.py` fetches live fixtures.**
It calls `GET /fixtures?live=all`, which returns every match in play
right now across all competitions, then `normalize_fixture()` reshapes
each one into the flat schema the frontend consumes (same shape as
`frontend/src/data/mockData.js`, so frontend/backend never drift apart).

**4. `app/main.py` runs a polling loop as a background task.**
On startup, it kicks off `poll_loop()`, which every `POLL_INTERVAL_SECONDS`
(default 20s):
- calls the provider for fresh fixture data,
- diffs each fixture's events against the last snapshot
  (`app/event_detector.py`) to find anything *new* (a goal that wasn't
  there last poll, a card that just appeared),
- broadcasts the full updated match over WebSocket to every connected
  browser tab (`app/websocket_manager.py`),
- and passes any brand-new events to `app/social_poster.py`.

A polling loop (rather than a raw websocket straight from the provider)
is what most commercial football APIs actually offer at this price
point — true push websockets are usually an enterprise/Sportradar-tier
feature. 15–30s polling feels live enough for goals/cards without
hammering your rate limit.

**5. The frontend connects to `/ws/live`.**
`frontend/src/hooks/useLiveScores.js` opens a WebSocket, receives a
`snapshot` on connect and `update` messages as they happen, and updates
React state — no page refresh, no polling on the client side.

**6. New events optionally get posted to social media.**
`app/social_poster.py` formats a short line like
`⚽ GOAL! B. Saka (Arsenal) — Arsenal 2 Chelsea 1 [63']` and posts it to
X and Facebook. Set `ENABLE_SOCIAL_POSTING=true` and fill in the
platform credentials in `.env` once you've registered developer apps
(instructions are in the docstring at the top of `social_poster.py`).
TikTok is a special case — see that file for why (it needs a rendered
video, not a text post).

## Run it

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then fill in API_FOOTBALL_KEY
uvicorn app.main:app --reload --port 8000
```

Check it's alive:
```bash
curl http://localhost:8000/api/fixtures/live
```

Then run the frontend (`frontend/README.md`) with
`VITE_WS_URL=ws://localhost:8000/ws/live` and you should see live
matches flow in as soon as any fixture from your provider is in play
(during off-hours with no live matches, `_last_snapshot` will just be
empty — that's expected, not a bug).

## Production notes

- **Scale beyond one process**: `_last_snapshot` and `ConnectionManager`
  are in-memory. For multiple backend workers/instances, move the
  snapshot to Redis and use a pub/sub channel (e.g. Redis Pub/Sub or
  a message queue) so every instance broadcasts the same events instead
  of duplicating or missing them.
- **Rate limits**: check your provider plan's requests/minute cap and
  set `POLL_INTERVAL_SECONDS` accordingly — polling too fast will get
  you throttled or billed extra.
- **Lineups**: `fetch_lineups()` is stubbed in the client; call it once
  per fixture near kickoff and cache it (lineups don't change once
  submitted) rather than polling it alongside live scores.
- **Deploy**: any ASGI host works — Fly.io, Railway, Render, or a plain
  VM behind nginx with `uvicorn` + `--workers`. Make sure your host
  supports long-lived WebSocket connections.
