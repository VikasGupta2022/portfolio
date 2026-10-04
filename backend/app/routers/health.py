from datetime import datetime
from fastapi import APIRouter
from app.config import settings
from app.database import active_db_type

router = APIRouter(tags=["Health"])

@router.get("/api/health", summary="Health Check")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database_backend": active_db_type,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
