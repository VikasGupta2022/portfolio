import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory for the backend
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Vikas Gupta Portfolio API")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() in ("true", "1", "yes")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("PORT", os.getenv("APP_PORT", "8000")))

    # CORS
    raw_cors: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000,http://127.0.0.1:8000,https://portfolio-frontend-delta-woad.vercel.app"
    )
    CORS_ORIGINS: list[str] = [origin.strip() for origin in raw_cors.split(",") if origin.strip()]

    # Database
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "vikas_portfolio_db")
    ENABLE_SQLITE_FALLBACK: bool = os.getenv("ENABLE_SQLITE_FALLBACK", "true").lower() in ("true", "1", "yes")

    # Email notification target
    RECEIVER_EMAIL: str = os.getenv("RECEIVER_EMAIL", "vikasgupta2020vg@gmail.com")

    @property
    def mysql_database_url(self) -> str:
        # Construct MySQL connection URL using PyMySQL driver
        # mysql+pymysql://<user>:<password>@<host>:<port>/<dbname>?charset=utf8mb4
        auth = f"{self.DB_USER}:{self.DB_PASSWORD}" if self.DB_PASSWORD else self.DB_USER
        return f"mysql+pymysql://{auth}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

    @property
    def sqlite_database_url(self) -> str:
        db_file = BASE_DIR / "portfolio_local.db"
        return f"sqlite:///{db_file}"

settings = Settings()
