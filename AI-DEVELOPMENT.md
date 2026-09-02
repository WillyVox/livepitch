What's in the zip

frontend/ — React + Vite + Tailwind. Scoreboard-style dark UI (turf-green/signal-orange accents, condensed display type for scores), fully responsive. Home feed of live matches grouped by league, a match detail page with an event timeline and lineup pitch view, and a useLiveScores hook that opens a WebSocket to your backend and falls back to mock data if it's not running — so npm install && npm run dev gives you a working preview immediately.

backend/ — FastAPI + WebSocket. app/livescore_client.py is an adapter around API-FOOTBALL (api-sports.io) that normalizes their fixture schema into the same flat shape the frontend expects. app/main.py runs a background polling loop, diffs each poll against the last snapshot (event_detector.py) to catch new goals/cards, broadcasts to all connected browsers, and optionally fires off posts to X/Facebook (social_poster.py).

The data pipeline, in short
Buy an API-FOOTBALL key (or swap the adapter for LiveScore API / SportMonks / Sportradar — same interface).
Backend polls /fixtures?live=all every ~20s (tune to your plan's rate limit).
It diffs events per fixture to catch new goals/cards only.
Pushes updates over /ws/live → frontend re-renders instantly, no refresh.
New events optionally get posted to X and Facebook automatically.

A few things worth flagging honestly:

True push websockets from the provider are rare below enterprise tiers — polling every 15–30s is what most commercial football APIs actually give you, and it reads as "live" in practice.
TikTok has no text-post API. Posting there means rendering a short video clip per event and going through their (app-reviewed) Content Posting API — I stubbed this out with the reasoning in social_poster.py rather than pretending it's a simple call.
Both READMEs (frontend/README.md, backend/README.md) have full setup steps and production notes (Redis for multi-instance state, rate limits, lineup caching).