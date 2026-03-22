const severityColors = {
  CRITICAL: "#ff0040",
  WARNING: "#ffaa00",
  NORMAL: "#00ff00",
  UNKNOWN: "#336633",
}

export default function LogTable({ logs }) {
  if (!logs.length) {
    return <div className="text-green-900 text-xs tracking-widest animate-pulse">// AWAITING_LOG_DATA...</div>
  }

  return (
    <div className="overflow-x-auto max-h-72 overflow-y-auto">
      <table className="w-full text-xs font-mono">
        <thead>
          <tr className="border-b border-green-900 text-green-700 tracking-widest">
            <th className="pb-2 pr-6 text-left">SEVERITY</th>
            <th className="pb-2 pr-6 text-left">TYPE</th>
            <th className="pb-2 pr-6 text-left">SOURCE_IP</th>
            <th className="pb-2 pr-6 text-left">CATEGORY</th>
            <th className="pb-2 text-left">ACTION</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, i) => {
            const color = severityColors[log.severity] || "#336633"
            return (
              <tr key={i}
                className="border-b border-green-950 hover:bg-green-950 hover:bg-opacity-30 transition-colors"
                style={{ borderColor: "#001100" }}>
                <td className="py-1.5 pr-6 font-black tracking-widest"
                  style={{ color, textShadow: `0 0 8px ${color}` }}>
                  {log.severity}
                </td>
                <td className="py-1.5 pr-6 text-green-600">{log.type}</td>
                <td className="py-1.5 pr-6 text-green-700">{log.ip || log.src_ip || "N/A"}</td>
                <td className="py-1.5 pr-6 text-green-800">{log.category}</td>
                <td className="py-1.5 font-black" style={{ color }}>{log.recommended_action}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}