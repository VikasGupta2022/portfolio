import os
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.database import engine, Base, SessionLocal, active_db_type
from app.routers import contact_router, projects_router, health_router
from app.services.project_service import seed_default_projects

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.APP_DEBUG else logging.WARNING,
    format="%(asctime)s - [%(levelname)s] - %(name)s: %(message)s"
)
logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle management.
    Initializes tables and seeds initial project records.
    """
    logger.info(f"🚀 Starting {settings.APP_NAME}...")
    logger.info(f"📊 Active Database Backend: {active_db_type.upper()}")
    try:
        # Create database tables if they do not exist
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables verified/created successfully.")

        # Seed initial default projects if empty
        with SessionLocal() as db:
            seed_default_projects(db)
    except Exception as e:
        logger.error(f"❌ Database initialization notice: {e}")

    yield
    logger.info(f"🛑 Shutting down {settings.APP_NAME}...")

# Initialize FastAPI instance
app = FastAPI(
    title=settings.APP_NAME,
    description="REST API backend for Vikas Gupta's software engineering portfolio website.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health_router)
app.include_router(contact_router)
app.include_router(projects_router)

# Mount frontend directory for seamless full-stack single-port serving
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
    logger.info(f"📂 Mounting frontend static files from: {FRONTEND_DIR}")
    # Mount images, css, js, assets
    for sub in ["css", "js", "images", "assets"]:
        subpath = FRONTEND_DIR / sub
        if subpath.exists():
            app.mount(f"/{sub}", StaticFiles(directory=str(subpath)), name=sub)

    @app.get("/", include_in_schema=False)
    async def serve_index():
        index_file = FRONTEND_DIR / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": "Welcome to Vikas Gupta Portfolio API. Frontend index.html not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG
    )
