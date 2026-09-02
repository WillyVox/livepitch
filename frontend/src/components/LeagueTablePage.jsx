import { useParams, Link, useNavigate } from 'react-router-dom'
import { mockLeagues } from '../data/mockData'
import { useStandings } from '../hooks/useStandings'
import LeagueTable from './LeagueTable'

export default function LeagueTablePage() {
  const { leagueId } = useParams()
  const navigate = useNavigate()
  const league = mockLeagues.find((l) => l.id === leagueId) || mockLeagues[0]
  const { standings, loading, isLive } = useStandings(league.id)

  return (
    <div className="mx-auto max-w-4xl px-4 py-6 md:px-6">
      <Link to="/" className="text-sm text-pitch-greenBright">
        ← Back to matches
      </Link>

      <div className="mt-4 mb-5 flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-pitch-muted">{league.country}</p>
          <h1 className="font-display text-3xl font-800 text-pitch-text">{league.name} table</h1>
        </div>
        <span className="text-xs text-pitch-muted">
          {isLive ? 'Updated live' : 'Preview data'}
        </span>
      </div>

      <div className="scrollbar-thin mb-5 flex gap-1 overflow-x-auto border-b border-pitch-line pb-2">
        {mockLeagues.map((l) => (
          <button
            key={l.id}
            onClick={() => navigate(`/table/${l.id}`)}
            className={`shrink-0 rounded-sm px-3 py-1.5 text-sm transition ${
              l.id === league.id
                ? 'bg-pitch-surface2 text-pitch-text'
                : 'text-pitch-muted hover:text-pitch-text'
            }`}
          >
            {l.name}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="px-1 py-8 text-sm text-pitch-muted">Loading table…</p>
      ) : (
        <LeagueTable standings={standings} highlightTop={4} highlightBottom={3} />
      )}

      <p className="mt-3 text-xs text-pitch-muted">
        <span className="mr-1 inline-block h-1.5 w-1.5 rounded-full bg-pitch-greenBright" />
        Continental qualification
        <span className="ml-4 mr-1 inline-block h-1.5 w-1.5 rounded-full bg-pitch-live" />
        Relegation zone
      </p>
    </div>
  )
}
