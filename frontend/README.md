# LivePitch — Frontend

React + Vite + Tailwind live football scores UI.

## Setup

```bash
npm install
cp .env.example .env   # point VITE_WS_URL at your backend
npm run dev
```

Opens on http://localhost:5173. Works standalone with mock data even
without the backend running (see `src/data/mockData.js` and
`src/hooks/useLiveScores.js`), so you can preview the UI immediately.

## Structure

- `src/components/` — Navbar, LeagueSidebar, MatchCard/Grid, MatchDetail, LineupPitch
- `src/hooks/useLiveScores.js` — opens a WebSocket to `VITE_WS_URL` and keeps
  match state in sync; expects messages shaped like:
  ```json
  { "type": "snapshot", "matches": [ ... ] }
  { "type": "update", "match": { ... } }
  ```
- `src/data/mockData.js` — fallback/demo data matching the same shape the
  backend sends, so backend and frontend schemas stay in lockstep.

## Deploy

`npm run build` outputs static files in `dist/` — deploy to Vercel,
Netlify, Cloudflare Pages, or any static host. Point `VITE_WS_URL` at your
production backend's `wss://` endpoint.
