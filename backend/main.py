from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from alert_manager import run_analysis_pipeline
from db import get_recent_logs, get_alerts, get_stats
import asyncio
import json

app = FastAPI(title="NetGuard AI", version="1.0.0")

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active websocket connections
active_connections: list[WebSocket] = []

async def broadcast(data: dict):
    for connection in active_connections:
        try:
            await connection.send_text(json.dumps(data))
        except:
            pass

@app.get("/")
def root():
    return {"status": "NetGuard AI is running"}

@app.get("/logs")
def fetch_logs():
    return get_recent_logs(50)

@app.get("/alerts")
def fetch_alerts():
    return get_alerts(50)

@app.get("/stats")
def fetch_stats():
    return get_stats()

@app.post("/analyze")
async def trigger_analysis():
    enriched = run_analysis_pipeline(n_logs=10)
    for log in enriched:
        if log.get("severity") in ["CRITICAL", "WARNING"]:
            await broadcast(log)
    return {"analyzed": len(enriched), "results": enriched}
@app.websocket("/ws/live-feed")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await asyncio.sleep(30)
            # Auto-analyze every 30 seconds and push alerts
            enriched = run_analysis_pipeline(n_logs=5)
            for log in enriched:
                if log.get("severity") in ["CRITICAL", "WARNING"]:
                    await broadcast(log)
    except WebSocketDisconnect:
        active_connections.remove(websocket)