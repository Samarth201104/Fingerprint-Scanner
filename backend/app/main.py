from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.api.routes import fingerprint, health
from backend.app.core.config import CORS_ORIGINS

app = FastAPI(title="Fingerprint Scanner AI", version="1.0.0", description="Camera-based fingerprint image acquisition and enhancement system.")
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])
app.include_router(health.router, prefix="/api/v1")
app.include_router(fingerprint.router, prefix="/api/v1/fingerprint", tags=["fingerprint"])


@app.exception_handler(Exception)
async def unhandled_error(_: Request, __: Exception):
    return JSONResponse(status_code=500, content={"success": False, "message": "An unexpected server error occurred.", "error_code": "INTERNAL_ERROR"})
