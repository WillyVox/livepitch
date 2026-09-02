import { mockLeagues } from '../data/mockData'

export default function LeagueSidebar({ selected, onSelect }) {
  return (
    <aside className="scrollbar-thin overflow-x-auto border-b border-pitch-line md:w-56 md:shrink-0 md:overflow-visible md:border-b-0 md:border-r">
      <nav className="flex gap-1 px-4 py-3 md:flex-col md:px-3 md:py-4">
        <button
          onClick={() => onSelect('all')}
          className={`shrink-0 rounded-sm px-3 py-2 text-left text-sm transition ${
            selected === 'all'
              ? 'bg-pitch-surface2 text-pitch-text'
              : 'text-pitch-muted hover:text-pitch-text'
          }`}
        >
          All matches
        </button>
        {mockLeagues.map((league) => (
          <button
            key={league.id}
            onClick={() => onSelect(league.name)}
            className={`shrink-0 rounded-sm px-3 py-2 text-left text-sm transition ${
              selected === league.name
                ? 'bg-pitch-surface2 text-pitch-text'
                : 'text-pitch-muted hover:text-pitch-text'
            }`}
          >
            <span className="block">{league.name}</span>
            <span className="hidden text-xs text-pitch-muted md:block">{league.country}</span>
          </button>
        ))}
      </nav>
    </aside>
  )
}
