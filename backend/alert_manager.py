from db import save_logs, get_recent_logs, get_alerts, get_stats
from log_generator import generate_bulk_logs
from log_parser import parse_bulk_logs
from ai_analyzer import analyze_logs
from bson import ObjectId

def clean_doc(doc: dict) -> dict:
    """Remove or convert any MongoDB ObjectId fields"""
    return {k: (str(v) if isinstance(v, ObjectId) else v) for k, v in doc.items()}

def run_analysis_pipeline(n_logs: int = 10) -> list[dict]:
    raw_logs = generate_bulk_logs(n_logs)
    parsed = parse_bulk_logs(raw_logs)
    enriched = analyze_logs(parsed)
    save_logs(enriched)
    # Clean docs before returning to FastAPI
    return [clean_doc(doc) for doc in enriched]