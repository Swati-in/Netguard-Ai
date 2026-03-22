import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, LineChart, Line } from "recharts"

const COLORS = {
  BRUTE_FORCE: "#ff0040",
  PORT_SCAN: "#ff6600",
  SUSPICIOUS_HTTP: "#ffaa00",
  FIREWALL_BLOCK: "#aa00ff",
  NORMAL_TRAFFIC: "#00ff00",
  DATA_EXFILTRATION: "#ff00aa",
  UNKNOWN: "#336633",
}

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="border border-green-700 bg-black p-3 text-xs font-mono"
        style={{ boxShadow: "0 0 15px #00ff0044" }}>
        <p className="text-green-400 font-black">{label}</p>
        <p className="text-green-300">COUNT: {payload[0].value}</p>
      </div>
    )
  }
  return null
}

export default function ThreatChart({ data }) {
  if (!data.length) {
    return <div className="text-green-900 text-xs tracking-widest animate-pulse">// NO_DATA</div>
  }

  const chartData = data.map(item => ({
    name: (item._id || "UNKNOWN").replace("_", " "),
    count: item.count,
    fill: COLORS[(item._id || "UNKNOWN")] || "#336633"
  }))

  return (
    <ResponsiveContainer width="100%" height={250}>
      <BarChart data={chartData} barCategoryGap="30%">
        <XAxis
          dataKey="name"
          tick={{ fill: "#336633", fontSize: 9, fontFamily: "monospace", fontWeight: "bold" }}
          axisLine={{ stroke: "#003300" }}
          tickLine={false}
        />
        <YAxis
          tick={{ fill: "#336633", fontSize: 10, fontFamily: "monospace" }}
          axisLine={{ stroke: "#003300" }}
          tickLine={false}
        />
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey="count" radius={[2, 2, 0, 0]}>
          {chartData.map((entry, index) => (
            <Cell
              key={index}
              fill={entry.fill}
              style={{ filter: `drop-shadow(0 0 6px ${entry.fill})` }}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}