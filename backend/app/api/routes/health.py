from fastapi import APIRouter
from backend.app.schemas.common import ApiResponse

router = APIRouter()


@router.get("/health", response_model=ApiResponse)
def health():
    return {"success": True, "message": "Fingerprint Scanner API is ready", "data": {"status": "healthy"}}
