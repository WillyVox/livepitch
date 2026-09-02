// Simple formation renderer: expects lineups like
// { formation: '4-3-3', players: [{ name, x, y }] } with x,y in 0-100 (%)
const demoFormation = {
  formation: '4-3-3',
  players: [
    { name: 'Raya', x: 50, y: 94 },
    { name: 'White', x: 18, y: 76 },
    { name: 'Saliba', x: 38, y: 80 },
    { name: 'Gabriel', x: 62, y: 80 },
    { name: 'Zinchenko', x: 82, y: 76 },
    { name: 'Rice', x: 35, y: 56 },
    { name: 'Odegaard', x: 50, y: 48 },
    { name: 'Havertz', x: 65, y: 56 },
    { name: 'Saka', x: 20, y: 26 },
    { name: 'Jesus', x: 50, y: 16 },
    { name: 'Martinelli', x: 80, y: 26 },
  ],
}

export default function LineupPitch({ teamName = 'Home', data = demoFormation }) {
  return (
    <div className="rounded-sm border border-pitch-line bg-pitch-surface p-4">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="font-display text-lg text-pitch-text">{teamName}</h3>
        <span className="text-xs text-pitch-muted">{data.formation}</span>
      </div>
      <div
        className="relative w-full overflow-hidden rounded-sm border border-pitch-line"
        style={{
          aspectRatio: '3 / 4',
          background:
            'repeating-linear-gradient(0deg, #163a24 0, #163a24 10%, #12321f 10%, #12321f 20%)',
        }}
      >
        <div className="absolute left-1/2 top-1/2 h-16 w-16 -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/20" />
        {data.players.map((p) => (
          <div
            key={p.name}
            className="absolute flex -translate-x-1/2 -translate-y-1/2 flex-col items-center"
            style={{ left: `${p.x}%`, top: `${p.y}%` }}
          >
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-pitch-bg text-[10px] font-semibold text-pitch-text ring-1 ring-white/30">
              {p.name[0]}
            </span>
            <span className="mt-1 whitespace-nowrap text-[10px] text-white/80">{p.name}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
