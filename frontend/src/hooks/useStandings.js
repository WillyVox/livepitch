import { useEffect, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Fetches standings for a given league id from the backend
 * (GET /api/standings/{leagueId}). Falls back to mock data if the
 * backend isn't reachable, so the table is always demoable.
 */
export function useStandings(leagueId) {
  const [standings, setStandings] = useState([])
  const [loading, setLoading] = useState(true)
  const [isLive, setIsLive] = useState(false)

  useEffect(() => {
    if (!leagueId) return
    let cancelled = false
    setLoading(true)
    setStandings([])

    fetch(`${API_URL}/api/standings/${leagueId}`)
      .then((res) => {
        if (!res.ok) throw new Error('Standings request failed')
        return res.json()
      })
      .then((data) => {
        if (!cancelled && Array.isArray(data.standings) && data.standings.length > 0) {
          setStandings(data.standings)
          setIsLive(true)
        }
      })
      .catch(() => {
        // Backend not available yet — mock data set above stays as-is.
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [leagueId])

  return { standings, loading, isLive }
}
