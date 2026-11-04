import certifi
from pymongo import MongoClient
from backend.app.core.config import settings
from backend.app.db.mongodb import check_mongo_health, log_mongo_audit_event

def test_connection():
    if not settings.MONGODB_URI:
        print("MONGODB_URI is not set.")
        return False
    health = check_mongo_health()
    print("Health check result:", health)
    
    # Test audit logging
    ok = log_mongo_audit_event("startup_ping", {"message": "PayMesh AI connected to MongoDB Atlas"})
    print("Audit event logged:", ok)
    return health.get("status") == "connected"

if __name__ == "__main__":
    test_connection()
