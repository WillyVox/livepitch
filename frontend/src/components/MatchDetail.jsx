import { useParams, Link } from 'react-router-dom'
import { mockMatches } from '../data/mockData'
import LineupPitch from './LineupPitch'

const icon = { goal: '⚽', yellow: '🟨', red: '🟥' }

export default function MatchDetail({ matches }) {
  const { id } = useParams()
  const match = (matches?.length ? matches : mockMatches).find((m) => m.id === id)

  if (!match) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-12">
        <Link to="/" className="text-sm text-pitch-greenBright">
          ← Back to all matches
        </Link>
        <p className="mt-4 text-pitch-muted">Match not found.</p>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-6 md:px-6">
      <Link to="/" className="text-sm text-pitch-greenBright">
        ← Back to all matches
      </Link>

      <div className="mt-4 border border-pitch-line bg-pitch-surface p-6 text-center">
        <p className="text-xs uppercase tracking-wide text-pitch-muted">{match.league}</p>
        <div className="mt-4 grid grid-cols-3 items-center gap-4">
          <span className="font-display text-2xl text-pitch-text">{match.home.name}</span>
          <span className="font-display text-5xl font-800 text-pitch-text">
            {match.home.score ?? '–'} : {match.away.score ?? '–'}
          </span>
          <span className="font-display text-2xl text-pitch-text">{match.away.name}</span>
        </div>
        <p className="mt-3 text-sm text-pitch-live">
          {match.status === 'LIVE' ? `Live · ${match.minute}'` : match.status}
        </p>
      </div>

      <div className="mt-8">
        <h2 className="mb-3 font-display text-xl text-pitch-text">Match events</h2>
        <ol className="space-y-2 border-l border-pitch-line pl-4">
          {match.events.length === 0 && (
            <li className="text-sm text-pitch-muted">No events yet.</li>
          )}
          {match.events.map((e, i) => (
            <li key={i} className="text-sm text-pitch-text">
              <span className="text-pitch-muted">{e.minute}&apos;</span> {icon[e.type]}{' '}
              {e.player}{' '}
              <span className="text-pitch-muted">
                ({e.team === 'home' ? match.home.name : match.away.name})
              </span>
            </li>
          ))}
        </ol>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <LineupPitch teamName={match.home.name} />
        <LineupPitch teamName={match.away.name} />
      </div>
    </div>
  )
}
