function FormDot({ result }) {
  const styles = {
    W: 'bg-pitch-greenBright text-pitch-bg',
    D: 'bg-pitch-amber text-pitch-bg',
    L: 'bg-pitch-live text-pitch-bg',
  }
  return (
    <span
      className={`flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold ${styles[result]}`}
    >
      {result}
    </span>
  )
}

export default function LeagueTable({ standings, highlightTop = 4, highlightBottom = 0 }) {
  if (!standings || standings.length === 0) {
    return <p className="px-4 py-8 text-center text-pitch-muted">No standings available.</p>
  }

  const total = standings.length

  return (
    <div className="scrollbar-thin overflow-x-auto border border-pitch-line">
      <table className="w-full min-w-[640px] border-collapse text-sm">
        <thead>
          <tr className="border-b border-pitch-line text-left text-xs uppercase tracking-wide text-pitch-muted">
            <th className="px-3 py-2 font-medium">#</th>
            <th className="px-3 py-2 font-medium">Club</th>
            <th className="px-2 py-2 text-center font-medium">P</th>
            <th className="px-2 py-2 text-center font-medium">W</th>
            <th className="px-2 py-2 text-center font-medium">D</th>
            <th className="px-2 py-2 text-center font-medium">L</th>
            <th className="px-2 py-2 text-center font-medium">GF</th>
            <th className="px-2 py-2 text-center font-medium">GA</th>
            <th className="px-2 py-2 text-center font-medium">GD</th>
            <th className="px-2 py-2 text-center font-medium">Pts</th>
            <th className="px-3 py-2 text-left font-medium">Form</th>
          </tr>
        </thead>
        <tbody>
          {standings.map((row) => {
            const gd = row.gf - row.ga
            const isTop = row.rank <= highlightTop
            const isBottom = highlightBottom > 0 && row.rank > total - highlightBottom
            return (
              <tr
                key={row.team}
                className="border-b border-pitch-line last:border-b-0 hover:bg-pitch-surface"
              >
                <td className="px-3 py-2.5">
                  <span className="flex items-center gap-2">
                    <span
                      className={`h-1.5 w-1.5 rounded-full ${
                        isTop ? 'bg-pitch-greenBright' : isBottom ? 'bg-pitch-live' : 'bg-transparent'
                      }`}
                    />
                    {row.rank}
                  </span>
                </td>
                <td className="px-3 py-2.5 font-medium text-pitch-text">{row.team}</td>
                <td className="px-2 py-2.5 text-center text-pitch-muted">{row.played}</td>
                <td className="px-2 py-2.5 text-center text-pitch-muted">{row.win}</td>
                <td className="px-2 py-2.5 text-center text-pitch-muted">{row.draw}</td>
                <td className="px-2 py-2.5 text-center text-pitch-muted">{row.loss}</td>
                <td className="px-2 py-2.5 text-center text-pitch-muted">{row.gf}</td>
                <td className="px-2 py-2.5 text-center text-pitch-muted">{row.ga}</td>
                <td className="px-2 py-2.5 text-center text-pitch-muted">
                  {gd > 0 ? `+${gd}` : gd}
                </td>
                <td className="px-2 py-2.5 text-center font-display text-base font-700 text-pitch-text">
                  {row.points}
                </td>
                <td className="px-3 py-2.5">
                  <span className="flex gap-1">
                    {row.form.map((r, i) => (
                      <FormDot key={i} result={r} />
                    ))}
                  </span>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
