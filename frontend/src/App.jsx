import { useState, useEffect, useRef } from "react"
import axios from "axios"
import StatCard from "./components/StatCard"
import AlertFeed from "./components/AlertFeed"
import ThreatChart from "./components/ThreatChart"
import LogTable from "./components/LogTable"

const API = "http://127.0.0.1:8000"

export default function App() {
  const [stats, setStats] = useState({ total: 0, critical: 0, warning: 0, normal: 0, by_category: [] })
  const [alerts, setAlerts] = useState([])
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)
  const [lastUpdated, setLastUpdated] = useState(null)
  const [liveAlert, setLiveAlert] = useState(null)
  const [glitch, setGlitch] = useState(false)
  const wsRef = useRef(null)

  const fetchData = async () => {
    try {
      const [statsRes, alertsRes, logsRes] = await Promise.all([
        axios.get(`${API}/stats`),
        axios.get(`${API}/alerts`),
        axios.get(`${API}/logs`),
      ])
      setStats(statsRes.data)
      setAlerts(alertsRes.data)
      setLogs(logsRes.data)
      setLastUpdated(new Date().toLocaleTimeString())
    } catch (err) {
      console.error("Fetch error:", err)
    }
  }

  const runAnalysis = async () => {
    setLoading(true)
    setGlitch(true)
    setTimeout(() => setGlitch(false), 600)
    try {
      await axios.post(`${API}/analyze`, {}, { timeout: 60000 })
      await fetchData()
    } catch (err) {
      console.error("Analysis error:", err)
    }
    setLoading(false)
  }

  useEffect(() => {
    wsRef.current = new WebSocket(`ws://127.0.0.1:8000/ws/live-feed`)
    wsRef.current.onmessage = (event) => {
      const alert = JSON.parse(event.data)
      setLiveAlert(alert)
      setTimeout(() => setLiveAlert(null), 8000)
    }
    return () => wsRef.current?.close()
  }, [])

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-black text-green-400 font-mono overflow-x-hidden" style={{background: "radial-gradient(ellipse at top, #001a00 0%, #000000 70%)"}}>
      
      {/* Scanline overlay */}
      <div className="fixed inset-0 pointer-events-none z-50" style={{
        background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,0,0.015) 2px, rgba(0,255,0,0.015) 4px)"
      }}/>

      {/* Matrix rain canvas */}
      <MatrixRain />

      <div className="relative z-10 p-6 max-w-7xl mx-auto">

        {/* Header */}
        <div className="flex items-center justify-between mb-8 border-b border-green-900 pb-6">
          <div>
            <div className={`text-4xl font-black tracking-widest text-green-400 ${glitch ? "animate-pulse" : ""}`}
              style={{textShadow: "0 0 20px #00ff00, 0 0 40px #00ff00, 0 0 80px #00ff00"}}>
              ▓ NETGUARD_AI
            </div>
            <div className="text-green-700 text-xs tracking-widest mt-1">
              // INTRUSION_DETECTION_SYSTEM v1.0.0 — STATUS: <span className="text-green-400 animate-pulse">ACTIVE</span>
            </div>
          </div>
          <div className="flex items-center gap-6">
            {lastUpdated && (
              <div className="text-green-800 text-xs">
                LAST_SYNC: <span className="text-green-600">{lastUpdated}</span>
              </div>
            )}
            <button
              onClick={runAnalysis}
              disabled={loading}
              className="relative px-6 py-3 border border-green-500 text-green-400 text-sm font-black tracking-widest hover:bg-green-500 hover:text-black transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{boxShadow: loading ? "none" : "0 0 15px #00ff0066, inset 0 0 15px #00ff0011"}}
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <span className="animate-spin">◈</span> ANALYZING...
                </span>
              ) : "⚡ RUN_ANALYSIS"}
            </button>
          </div>
        </div>

        {/* Live Alert Banner */}
        {liveAlert && (
          <div className="mb-6 border border-red-500 bg-red-950 bg-opacity-50 p-4 animate-pulse"
            style={{boxShadow: "0 0 20px #ff000066"}}>
            <div className="text-red-400 text-xs font-black tracking-widest mb-1">
              ⚠ LIVE_THREAT_DETECTED // {liveAlert.category}
            </div>
            <div className="text-red-300 text-sm">{liveAlert.explanation}</div>
            <div className="text-red-600 text-xs mt-1">IP: {liveAlert.ip || liveAlert.src_ip} — ACTION: {liveAlert.recommended_action}</div>
          </div>
        )}

        {/* Stat Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatCard title="TOTAL_LOGS" value={stats.total} color="cyan" symbol="◈" />
          <StatCard title="CRITICAL" value={stats.critical} color="red" symbol="▲" />
          <StatCard title="WARNING" value={stats.warning} color="yellow" symbol="◆" />
          <StatCard title="NORMAL" value={stats.normal} color="green" symbol="●" />
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="border border-green-900 bg-black bg-opacity-80 p-5"
            style={{boxShadow: "inset 0 0 30px #00ff0008"}}>
            <div className="text-green-500 text-xs font-black tracking-widest mb-4 border-b border-green-900 pb-2">
              ▓ THREAT_ALERTS // LIVE_FEED
            </div>
            <AlertFeed alerts={alerts} />
          </div>

          <div className="border border-green-900 bg-black bg-opacity-80 p-5"
            style={{boxShadow: "inset 0 0 30px #00ff0008"}}>
            <div className="text-green-500 text-xs font-black tracking-widest mb-4 border-b border-green-900 pb-2">
              ▓ THREAT_DISTRIBUTION // CATEGORY_ANALYSIS
            </div>
            <ThreatChart data={stats.by_category} />
          </div>
        </div>

        {/* Log Table */}
        <div className="border border-green-900 bg-black bg-opacity-80 p-5"
          style={{boxShadow: "inset 0 0 30px #00ff0008"}}>
          <div className="text-green-500 text-xs font-black tracking-widest mb-4 border-b border-green-900 pb-2">
            ▓ RAW_LOG_STREAM // RECENT_ENTRIES
          </div>
          <LogTable logs={logs} />
        </div>

        {/* Footer */}
        <div className="mt-6 text-center text-green-900 text-xs tracking-widest">
          NETGUARD_AI // POWERED BY CLAUDE AI + MONGODB ATLAS // ALL THREATS LOGGED
        </div>
      </div>
    </div>
  )
}

function MatrixRain() {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext("2d")
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ"
    const fontSize = 14
    const columns = canvas.width / fontSize
    const drops = Array(Math.floor(columns)).fill(1)

    const draw = () => {
      ctx.fillStyle = "rgba(0, 0, 0, 0.05)"
      ctx.fillRect(0, 0, canvas.width, canvas.height)
      ctx.fillStyle = "#003300"
      ctx.font = `${fontSize}px monospace`
      drops.forEach((y, i) => {
        const char = chars[Math.floor(Math.random() * chars.length)]
        ctx.fillStyle = Math.random() > 0.98 ? "#00ff00" : "#003300"
        ctx.fillText(char, i * fontSize, y * fontSize)
        if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0
        drops[i]++
      })
    }

    const interval = setInterval(draw, 50)
    return () => clearInterval(interval)
  }, [])

  return <canvas ref={canvasRef} className="fixed inset-0 z-0 opacity-30" />
}