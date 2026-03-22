import { useEffect, useRef } from "react"

export default function StatCard({ title, value, color, symbol }) {
  const colors = {
    red: { border: "#ff0040", glow: "#ff004066", text: "#ff4466" },
    yellow: { border: "#ffaa00", glow: "#ffaa0066", text: "#ffcc00" },
    green: { border: "#00ff00", glow: "#00ff0066", text: "#00ff00" },
    cyan: { border: "#00ffff", glow: "#00ffff66", text: "#00ffff" },
  }
  const c = colors[color]

  return (
    <div className="relative border bg-black bg-opacity-90 p-5 overflow-hidden"
      style={{ borderColor: c.border, boxShadow: `0 0 20px ${c.glow}, inset 0 0 20px ${c.glow}22` }}>
      {/* Corner decorations */}
      <div className="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2" style={{ borderColor: c.border }} />
      <div className="absolute top-0 right-0 w-3 h-3 border-t-2 border-r-2" style={{ borderColor: c.border }} />
      <div className="absolute bottom-0 left-0 w-3 h-3 border-b-2 border-l-2" style={{ borderColor: c.border }} />
      <div className="absolute bottom-0 right-0 w-3 h-3 border-b-2 border-r-2" style={{ borderColor: c.border }} />

      <div className="text-2xl mb-2 opacity-60" style={{ color: c.text }}>{symbol}</div>
      <div className="text-5xl font-black mb-1 tabular-nums"
        style={{ color: c.text, textShadow: `0 0 20px ${c.border}` }}>
        {value}
      </div>
      <div className="text-xs tracking-widest opacity-60" style={{ color: c.text }}>
        {title}
      </div>
    </div>
  )
}