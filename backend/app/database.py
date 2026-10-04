import logging
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import settings

logger = logging.getLogger("uvicorn.error")

Base = declarative_base()

def get_engine():
    """
    Attempts to connect to MySQL database first.
    If MySQL server is offline/unavailable and ENABLE_SQLITE_FALLBACK is True,
    gracefully switches to SQLite for seamless local execution.
    """
    mysql_url = settings.mysql_database_url
    try:
        engine = create_engine(
            mysql_url,
            pool_recycle=3600,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 3}
        )
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"✅ Connected successfully to MySQL database: {settings.DB_NAME} on {settings.DB_HOST}:{settings.DB_PORT}")
        return engine, "mysql"
    except Exception as e:
        logger.warning(f"⚠️ MySQL connection failed: {e}")
        if settings.ENABLE_SQLITE_FALLBACK:
            sqlite_url = settings.sqlite_database_url
            logger.info(f"🔄 Switching to SQLite local fallback: {sqlite_url}")
            engine = create_engine(
                sqlite_url,
                connect_args={"check_same_thread": False}
            )
            return engine, "sqlite"
        raise e

engine, active_db_type = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection for FastAPI routes.
    Yields database session and guarantees closure.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
