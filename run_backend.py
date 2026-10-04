"""
Convenience entry point to launch the Vikas Gupta Portfolio FastAPI backend.
Usage: python run_backend.py
"""
import sys
import os
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("  Vikas Gupta - Portfolio & REST API Server")
    print("  Backend: FastAPI (Python 3.13)")
    print("  URL: http://127.0.0.1:8000")
    print("  Docs: http://127.0.0.1:8000/docs")
    print("=" * 60)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
