import { useEffect, useRef } from "react"

const severityConfig = {
  CRITICAL: { color: "#ff0040", label: "CRIT", bg: "#ff004022" },
  WARNING: { color: "#ffaa00", label: "WARN", bg: "#ffaa0022" },
  NORMAL: { color: "#00ff00", label: "NORM", bg: "#00ff0011" },
  UNKNOWN: { color: "#666666", label: "UNKN", bg: "#66666611" },
}

export default function AlertFeed({ alerts }) {
  if (!alerts.length) {
    return (
      <div className="text-green-900 text-xs tracking-widest animate-pulse">
        // AWAITING_THREAT_DATA... RUN ANALYSIS TO BEGIN
      </div>
    )
  }

  return (
    <div className="space-y-2 max-h-96 overflow-y-auto pr-1 scrollbar-thin">
      {alerts.map((alert, i) => {
        const cfg = severityConfig[alert.severity] || severityConfig.UNKNOWN
        return (
          <div key={i}
            className="border p-3 transition-all duration-300 hover:scale-[1.01]"
            style={{
              borderColor: cfg.color + "44",
              background: cfg.bg,
              boxShadow: `0 0 10px ${cfg.color}11`
            }}>
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-black tracking-widest px-2 py-0.5 border"
                style={{ color: cfg.color, borderColor: cfg.color, boxShadow: `0 0 8px ${cfg.color}66` }}>
                [{cfg.label}]
              </span>
              <span className="text-xs opacity-50" style={{ color: cfg.color }}>
                {alert.type} // {alert.category}
              </span>
            </div>
            <p className="text-xs text-green-300 leading-relaxed">{alert.explanation}</p>
            <div className="flex justify-between mt-2">
              <span className="text-xs opacity-40 text-green-600 font-mono">
                {alert.ip || alert.src_ip || "N/A"}
              </span>
              <span className="text-xs font-black tracking-widest" style={{ color: cfg.color }}>
                → {alert.recommended_action}
              </span>
            </div>
          </div>
        )
      })}
    </div>
  )
}