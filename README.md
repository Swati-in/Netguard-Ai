# 🛡️ NetGuard AI

### AI-Powered Real-Time Network Threat Detection Platform

> NetGuard AI ingests network logs, analyzes them using Claude AI, and displays live threat intelligence on a cyberpunk-themed security dashboard.

<img width="1920" height="1080" alt="Screenshot (702)" src="https://github.com/user-attachments/assets/95ecf9fd-251e-40c7-ad85-cd9084fc5c48" />
<img width="1920" height="1080" alt="Screenshot (703)" src="https://github.com/user-attachments/assets/557a9edf-1998-49c2-a03f-c4dbdf3e835c" />


---

## 🚀 Live Demo

| Service | Link |
|---|---|
| 🖥️ Dashboard | [Frontend on Vercel](#) |
| ⚙️ API Docs | [Backend on Railway](#) |

---

## 🧠 Architecture
```
Raw Logs → Log Parser → Claude AI → MongoDB Atlas → FastAPI → React Dashboard
                                         ↕
                                   WebSocket Feed
```

---

## ⚡ Features

- 🤖 **AI Threat Analysis** — Claude LLM classifies every log as CRITICAL / WARNING / NORMAL with plain-English explanations
- 🔴 **Live Alert Feed** — WebSocket-powered real-time threat notifications
- 📊 **Threat Dashboard** — Severity stats, category breakdown charts, full log table
- 🗄️ **Audit Trail** — Every threat persisted to MongoDB Atlas for historical analysis
- 🎯 **Attack Simulator** — Simulates SSH brute force, port scans, web exploits, and firewall storms
- 🌐 **REST API** — Full FastAPI backend with auto-generated Swagger docs

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| 🤖 AI Engine | Claude API (Anthropic) |
| ⚙️ Backend | Python 3.12, FastAPI, WebSockets |
| 🗄️ Database | MongoDB Atlas |
| 🎨 Frontend | React 18, Vite, Tailwind CSS v4, Recharts |
| 🔍 Log Analysis | Custom Python regex parsers |
| 🚀 Deployment | Vercel (frontend), Railway (backend) |

---

## 🚨 Threat Categories Detected

| Category | Description |
|---|---|
| `BRUTE_FORCE` | Repeated SSH login failures targeting user accounts |
| `PORT_SCAN` | Systematic port scanning for vulnerability reconnaissance |
| `SUSPICIOUS_HTTP` | Attempts to access `/etc/passwd`, `/.env`, `/wp-admin` |
| `FIREWALL_BLOCK` | Blocked connection attempts to sensitive ports |
| `DATA_EXFILTRATION` | Unusual outbound data transfer patterns |
| `NORMAL_TRAFFIC` | Legitimate network activity |

---

## 🏃 Run Locally

### Prerequisites
- Python 3.12+
- Node.js 22+
- MongoDB Atlas account
- Anthropic API key

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create `backend/.env`:
```env
ANTHROPIC_API_KEY=your_claude_api_key
MONGO_URI=your_mongodb_atlas_uri
DB_NAME=netguard
```

Start the server:
```bash
uvicorn main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Dashboard available at: `http://localhost:5173`

### Simulate an Attack
```bash
cd backend
python simulate_attack.py
```

Watch the dashboard light up with AI-detected threats in real time! 🔴

---

## 📁 Project Structure
```
netguard-ai/
├── backend/
│   ├── main.py              # FastAPI app + WebSocket server
│   ├── ai_analyzer.py       # Claude AI integration
│   ├── log_parser.py        # Regex-based log parsing engine
│   ├── log_generator.py     # Realistic fake log generator
│   ├── alert_manager.py     # Analysis pipeline orchestrator
│   ├── db.py                # MongoDB Atlas connection + queries
│   ├── simulate_attack.py   # Attack simulation scenarios
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.jsx                      # Main dashboard
│       └── components/
│           ├── StatCard.jsx             # Animated metric cards
│           ├── AlertFeed.jsx            # Live threat feed
│           ├── ThreatChart.jsx          # Category bar chart
│           └── LogTable.jsx             # Raw log stream table
├── .gitignore
└── README.md
```

---

## 🔐 Security Notes

- API keys stored in `.env` — never committed to version control
- MongoDB Atlas IP whitelisting enabled
- CORS configured for frontend-backend communication
- All threat data persisted for forensic audit trail

---

## 🎯 Use Cases

- **SOC Teams** — Real-time threat monitoring and triage
- **DevOps** — Infrastructure security visibility
- **Security Research** — Log analysis and threat pattern detection


## 👤 Author

**Swati Mohapatra**
- GitHub: [@Swati-in](https://github.com/Swati-in)
