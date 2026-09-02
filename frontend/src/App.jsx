import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import LeagueSidebar from './components/LeagueSidebar'
import MatchGrid from './components/MatchGrid'
import MatchDetail from './components/MatchDetail'
import { useLiveScores } from './hooks/useLiveScores'

function Home({ matches }) {
  const [league, setLeague] = useState('all')
  return (
    <div className="mx-auto flex max-w-7xl flex-col md:flex-row">
      <LeagueSidebar selected={league} onSelect={setLeague} />
      <main className="flex-1">
        <div className="border-b border-pitch-line px-4 py-4 md:px-6">
          <h1 className="font-display text-3xl font-800 text-pitch-text">
            {league === 'all' ? "Today's matches" : league}
          </h1>
          <p className="text-sm text-pitch-muted">Live scores, updated in real time</p>
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
      </Routes>
    </div>
  )
}
