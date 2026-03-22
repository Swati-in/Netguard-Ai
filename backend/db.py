from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

logs_collection = db["logs"]
alerts_collection = db["alerts"]

def fix_id(doc):
    """Convert ObjectId to string so FastAPI can serialize it"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

def save_logs(enriched_logs: list[dict]):
    if enriched_logs:
        result = logs_collection.insert_many(enriched_logs)
        return result

def get_recent_logs(limit: int = 50):
    return [fix_id(doc) for doc in logs_collection.find().sort("timestamp", -1).limit(limit)]

def get_alerts(limit: int = 50):
    return [fix_id(doc) for doc in logs_collection.find(
        {"severity": {"$in": ["CRITICAL", "WARNING"]}}
    ).sort("timestamp", -1).limit(limit)]

def get_stats():
    total = logs_collection.count_documents({})
    critical = logs_collection.count_documents({"severity": "CRITICAL"})
    warning = logs_collection.count_documents({"severity": "WARNING"})
    normal = logs_collection.count_documents({"severity": "NORMAL"})

    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    by_category = list(logs_collection.aggregate(pipeline))
    # Fix ObjectId in aggregation results too
    for item in by_category:
        if "_id" in item and isinstance(item["_id"], ObjectId):
            item["_id"] = str(item["_id"])

    return {
        "total": total,
        "critical": critical,
        "warning": warning,
        "normal": normal,
        "by_category": by_category
    }