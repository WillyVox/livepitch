import { Link } from 'react-router-dom'

const statusStyle = {
  LIVE: 'text-pitch-live',
  HT: 'text-pitch-amber',
  FT: 'text-pitch-muted',
  UPCOMING: 'text-pitch-muted',
}

function StatusBadge({ status, minute }) {
  if (status === 'LIVE') {
    return (
      <span className="flex items-center gap-1.5 text-xs font-semibold text-pitch-live">
        <span className="h-1.5 w-1.5 animate-pulseDot rounded-full bg-pitch-live" />
        {minute}&apos;
      </span>
    )
  }
  if (status === 'UPCOMING') return <span className="text-xs text-pitch-muted">Today</span>
  return <span className={`text-xs font-semibold ${statusStyle[status]}`}>{status}</span>
}

export default function MatchCard({ match }) {
  const lastEvent = match.events?.[match.events.length - 1]

  return (
    <Link
      to={`/match/${match.id}`}
      className="block border-b border-pitch-line px-4 py-3 transition hover:bg-pitch-surface md:px-5"
    >
      <div className="mb-2 flex items-center justify-between">
        <span className="text-xs uppercase tracking-wide text-pitch-muted">{match.league}</span>
        <StatusBadge status={match.status} minute={match.minute} />
      </div>

      <div className="grid grid-cols-[1fr_auto] items-center gap-3">
        <div className="space-y-1.5">
          <div className="flex items-center justify-between gap-3">
            <span className="font-medium text-pitch-text">{match.home.name}</span>
            <span className="font-display text-xl font-700 text-pitch-text">
              {match.home.score ?? '–'}
            </span>
          </div>
          <div className="flex items-center justify-between gap-3">
            <span className="font-medium text-pitch-text">{match.away.name}</span>
            <span className="font-display text-xl font-700 text-pitch-text">
              {match.away.score ?? '–'}
            </span>
          </div>
        </div>
      </div>

      {lastEvent && (
        <p className="mt-2 truncate text-xs text-pitch-muted">
          {lastEvent.minute}&apos; —{' '}
          {lastEvent.type === 'goal' ? '⚽' : lastEvent.type === 'yellow' ? '🟨' : '🟥'}{' '}
          {lastEvent.player}
        </p>
      )}

      {match.status === 'UPCOMING' && (
        <p className="mt-2 text-xs text-pitch-muted">Kick-off {match.kickoff}</p>
      )}
    </Link>
  )
}
