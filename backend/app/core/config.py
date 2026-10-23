from pathlib import Path
import os

BACKEND_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv("FINGERPRINT_DATA_DIR", BACKEND_DIR / "data" / "jobs"))
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", 12 * 1024 * 1024))
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/bmp", "image/webp", "application/octet-stream"}
DEFAULT_CORS_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001"
CORS_ORIGINS = [item.strip() for item in os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS).split(",") if item.strip()]
CORS_ORIGIN_REGEX = os.getenv("CORS_ORIGIN_REGEX") or None
