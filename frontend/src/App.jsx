import { useState } from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Navbar from './components/Navbar'
import LeagueSidebar from './components/LeagueSidebar'
import MatchGrid from './components/MatchGrid'
import MatchDetail from './components/MatchDetail'
import LeagueTablePage from './components/LeagueTablePage'
import { useLiveScores } from './hooks/useLiveScores'
import { mockLeagues } from './data/mockData'

function Home({ matches }) {
  const [league, setLeague] = useState('all')
  const selectedLeague = mockLeagues.find((l) => l.name === league)

  return (
    <div className="mx-auto flex max-w-7xl flex-col md:flex-row">
      <LeagueSidebar selected={league} onSelect={setLeague} />
      <main className="flex-1">
        <div className="flex flex-wrap items-end justify-between gap-3 border-b border-pitch-line px-4 py-4 md:px-6">
          <div>
            <h1 className="font-display text-3xl font-800 text-pitch-text">
              {league === 'all' ? "Today's matches" : league}
            </h1>
            <p className="text-sm text-pitch-muted">Live scores, updated in real time</p>
          </div>
          {selectedLeague && (
            <Link
              to={`/table/${selectedLeague.id}`}
              className="rounded-sm border border-pitch-line px-3 py-1.5 text-sm text-pitch-text transition hover:border-pitch-greenBright hover:text-pitch-greenBright"
            >
              View table
            </Link>
          )}
        </div>
        <MatchGrid matches={matches} league={league} />
      </main>
    </div>
  )
}

export default function App() {
  const { matches, connected } = useLiveScores()

  return (
    <div className="min-h-screen bg-pitch-bg">
      <Navbar connected={connected} />
      <Routes>
        <Route path="/" element={<Home matches={matches} />} />
        <Route path="/match/:id" element={<MatchDetail matches={matches} />} />
        <Route path="/table/:leagueId" element={<LeagueTablePage />} />
      </Routes>
    </div>
  )
}
