import { useEffect, useRef, useState } from 'react'
import { mockMatches } from '../data/mockData'

// Point this at your FastAPI backend, e.g. ws://localhost:8000/ws/live
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/live'

/**
 * Connects to the backend WebSocket and keeps a live map of matches
 * in state. Falls back to mock data (with light simulated movement)
 * if the backend isn't reachable, so the UI is always demoable.
 */
export function useLiveScores() {
  const [matches, setMatches] = useState(mockMatches)
  const [connected, setConnected] = useState(false)
  const socketRef = useRef(null)

  useEffect(() => {
    let fallbackTimer

    try {
      const socket = new WebSocket(WS_URL)
      socketRef.current = socket

      socket.onopen = () => setConnected(true)

      socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data)
          // Expected payload: { type: 'snapshot' | 'update', matches: [...] }
          if (payload.type === 'snapshot' && Array.isArray(payload.matches)) {
            setMatches(payload.matches)
          } else if (payload.type === 'update' && payload.match) {
            setMatches((prev) => {
              const idx = prev.findIndex((m) => m.id === payload.match.id)
              if (idx === -1) return [...prev, payload.match]
              const next = [...prev]
              next[idx] = payload.match
              return next
            })
          }
        } catch (e) {
          console.warn('Bad WS payload', e)
        }
      }

      socket.onclose = () => setConnected(false)
      socket.onerror = () => socket.close()
    } catch (e) {
      console.warn('WebSocket unavailable, using mock data', e)
    }

    // Demo-mode: gently nudge the clock on mock data so the UI feels alive
    // when no backend is connected. Harmless once real data arrives.
    fallbackTimer = setInterval(() => {
      setMatches((prev) =>
        prev.map((m) =>
          m.status === 'LIVE' ? { ...m, minute: Math.min(m.minute + 1, 90) } : m,
        ),
      )
    }, 15000)

    return () => {
      socketRef.current?.close()
      clearInterval(fallbackTimer)
    }
  }, [])

  return { matches, connected }
}
