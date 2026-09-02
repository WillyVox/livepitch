import MatchCard from './MatchCard'

const order = { LIVE: 0, HT: 1, UPCOMING: 2, FT: 3 }

export default function MatchGrid({ matches, league }) {
  const filtered = matches
    .filter((m) => league === 'all' || m.league === league)
    .sort((a, b) => order[a.status] - order[b.status])

  if (filtered.length === 0) {
    return (
      <div className="px-6 py-16 text-center text-pitch-muted">
        No matches in this league right now.
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-x-6 lg:grid-cols-2 xl:grid-cols-3">
      {filtered.map((m) => (
        <MatchCard key={m.id} match={m} />
      ))}
    </div>
  )
}
