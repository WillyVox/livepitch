import { Link } from 'react-router-dom'
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
          <div
            key={league.id}
            className={`group flex shrink-0 items-center justify-between rounded-sm px-3 py-2 transition ${
              selected === league.name ? 'bg-pitch-surface2' : 'hover:bg-pitch-surface2/50'
            }`}
          >
            <button
              onClick={() => onSelect(league.name)}
              className={`text-left text-sm ${
                selected === league.name ? 'text-pitch-text' : 'text-pitch-muted group-hover:text-pitch-text'
              }`}
            >
              <span className="block">{league.name}</span>
              <span className="hidden text-xs text-pitch-muted md:block">{league.country}</span>
            </button>
            <Link
              to={`/table/${league.id}`}
              title={`${league.name} table`}
              className="ml-2 shrink-0 text-xs text-pitch-muted transition hover:text-pitch-greenBright"
              onClick={(e) => e.stopPropagation()}
            >
              Table
            </Link>
          </div>
        ))}
      </nav>
    </aside>
  )
}
