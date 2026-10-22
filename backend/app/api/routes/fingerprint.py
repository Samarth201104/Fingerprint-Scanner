from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool
from pathlib import Path
import json
from backend.app.core.config import DATA_DIR
from backend.app.schemas.common import ApiResponse
from backend.app.core.config import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, MAX_UPLOAD_BYTES
from backend.app.core.logging import logger
from backend.app.services.fingerprint_service import fingerprint_service

router = APIRouter()


@router.get("/result/{job_id}")
def get_result(job_id: str):
    if not job_id.isalnum() or len(job_id) != 32:
        raise HTTPException(400, detail={"success": False, "message": "Invalid result identifier.", "error_code": "INVALID_ID"})
    result_path = DATA_DIR / job_id / "result.json"
    if not result_path.is_file():
        raise HTTPException(404, detail={"success": False, "message": "Processing result not found.", "error_code": "RESULT_NOT_FOUND"})
    return {"success": True, "message": "Processing result", "data": json.loads(result_path.read_text(encoding="utf-8"))}


def _result_path(job_id: str, stage: str) -> Path:
    if not job_id.isalnum() or len(job_id) != 32 or stage not in {"original", "roi", "preprocessed", "enhanced", "binary", "final"}:
        raise HTTPException(400, detail={"success": False, "message": "Invalid download request.", "error_code": "INVALID_DOWNLOAD"})
    path = DATA_DIR / job_id / f"{stage}.png"
    if not path.is_file():
        raise HTTPException(404, detail={"success": False, "message": "Processing result not found.", "error_code": "RESULT_NOT_FOUND"})
    return path


@router.get("/image/{job_id}/{stage}")
def view_result_image(job_id: str, stage: str):
    return FileResponse(_result_path(job_id, stage), media_type="image/png")


@router.get("/download/{job_id}/{stage}")
def download_result(job_id: str, stage: str):
    return FileResponse(_result_path(job_id, stage), media_type="image/png", filename=f"{stage}.png")


async def read_image(file: UploadFile) -> bytes:
    suffix = (file.filename or "").lower().rsplit(".", 1)
    extension = f".{suffix[-1]}" if len(suffix) > 1 else ""
    if extension not in ALLOWED_EXTENSIONS or (file.content_type and file.content_type not in ALLOWED_MIME_TYPES):
        raise HTTPException(415, detail={"success": False, "message": "Unsupported image type.", "error_code": "UNSUPPORTED_FILE"})
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if not content:
        raise HTTPException(400, detail={"success": False, "message": "The uploaded file is empty.", "error_code": "EMPTY_FILE"})
    if len(content) > MAX_UPLOAD_BYTES:
        limit_mb = MAX_UPLOAD_BYTES // (1024 * 1024)
        raise HTTPException(413, detail={"success": False, "message": f"Image exceeds the {limit_mb} MB upload limit.", "error_code": "FILE_TOO_LARGE"})
    return content


@router.post("/process", response_model=ApiResponse)
async def process_fingerprint(file: UploadFile = File(...), input_mode: str = Form(default="upload")):
    content = await read_image(file)
    logger.info("Processing request received mode=%s filename=%s", input_mode, file.filename)
    try:
        result = await run_in_threadpool(fingerprint_service.process_bytes, content, file.filename or "fingerprint", input_mode)
        logger.info("Fingerprint processing succeeded job_id=%s duration_ms=%s", result["job_id"], result["metadata"]["processing_time_ms"])
    except ValueError as exc:
        raise HTTPException(422, detail={"success": False, "message": str(exc), "error_code": "INVALID_IMAGE"}) from exc
    except Exception as exc:
        logger.exception("Fingerprint processing failed")
        raise HTTPException(500, detail={"success": False, "message": "Fingerprint processing failed.", "error_code": "PROCESSING_FAILED"}) from exc
    return {"success": True, "message": "Fingerprint processed successfully", "data": result}


@router.post("/validate", response_model=ApiResponse)
async def validate_fingerprint(file: UploadFile = File(...)):
    import cv2
    import numpy as np
    from backend.app.services.validation_service import inspect_quality
    content = await read_image(file)
    image = cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise HTTPException(422, detail={"success": False, "message": "The uploaded file is not a valid fingerprint image.", "error_code": "INVALID_IMAGE"})
    return {"success": True, "message": "Image validation completed", "data": inspect_quality(image)}


@router.post("/process-batch", response_model=ApiResponse)
async def process_fingerprint_batch(files: list[UploadFile] = File(...)):
    from backend.app.services.batch_service import process_batch
    if not files or len(files) > 50:
        raise HTTPException(400, detail={"success": False, "message": "Choose between 1 and 50 images.", "error_code": "INVALID_BATCH_SIZE"})
    inputs = []
    for file in files:
        try:
            inputs.append((file.filename or "fingerprint", await read_image(file)))
        except HTTPException as exc:
            inputs.append((file.filename or "fingerprint", b""))
    data = await run_in_threadpool(process_batch, inputs)
    for index, item in enumerate(data["results"]):
        if not item["success"] and not inputs[index][1]:
            item["error"] = "Unsupported file or empty upload."
    return {"success": True, "message": "Batch processing completed", "data": data}
