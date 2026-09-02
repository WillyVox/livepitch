import { Link } from 'react-router-dom'

export default function Navbar({ connected }) {
  return (
    <header className="sticky top-0 z-30 border-b border-pitch-line bg-pitch-bg/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 md:px-6">
        <Link to="/" className="flex items-baseline gap-2">
          <span className="font-display text-2xl font-800 tracking-tight text-pitch-text">
            LIVE<span className="text-pitch-greenBright">PITCH</span>
          </span>
        </Link>

        <div className="flex items-center gap-4">
          <div className="hidden items-center gap-1.5 text-xs text-pitch-muted md:flex">
            <span
              className={`h-1.5 w-1.5 rounded-full ${
                connected ? 'bg-pitch-greenBright' : 'bg-pitch-muted'
              }`}
            />
            {connected ? 'Live feed connected' : 'Demo mode'}
          </div>
          <button className="rounded-sm border border-pitch-line px-3 py-1.5 text-sm text-pitch-text transition hover:border-pitch-greenBright hover:text-pitch-greenBright">
            Sign in
          </button>
        </div>
      </div>
    </header>
  )
}
