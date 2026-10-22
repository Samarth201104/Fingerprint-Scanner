from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

import cv2
import numpy as np

from backend.pipeline.gabor_enhancement import gabor_enhance
from backend.pipeline.preprocessing import preprocess
from backend.pipeline.ridge_postprocess import postprocess
from backend.pipeline.roi_extraction import extract_roi
from backend.pipeline.thresholding import adaptive_threshold
from backend.app.services.validation_service import inspect_quality
from backend.app.core.config import DATA_DIR


class FingerprintService:
    def process_bytes(self, content: bytes, filename: str, input_mode: str = "upload") -> dict:
        started = time.perf_counter()
        raw = np.frombuffer(content, dtype=np.uint8)
        image = cv2.imdecode(raw, cv2.IMREAD_COLOR)
        if image is None or image.size == 0:
            raise ValueError("The uploaded file is not a valid fingerprint image.")
        height, width = image.shape[:2]
        if min(width, height) < 21:
            raise ValueError("Fingerprint images must be at least 21 pixels wide and high.")
        if width * height > 25_000_000:
            raise ValueError("Image dimensions exceed the 25 megapixel processing limit.")

        roi = extract_roi(image)
        if min(roi.shape[:2]) < 21:
            roi = image
        gray, normalized = preprocess(roi)
        enhanced = gabor_enhance(normalized)
        binary = adaptive_threshold(enhanced)
        final = postprocess(binary)
        source_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        quality = inspect_quality(source_gray)

        job_id = uuid.uuid4().hex
        images = {"original": image, "roi": roi, "preprocessed": normalized, "enhanced": enhanced, "binary": binary, "final": final}
        job_dir = DATA_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        for name, array in images.items():
            cv2.imwrite(str(job_dir / f"{name}.png"), array)
        safe_filename = filename.replace("\\", "/").split("/")[-1].replace("\x00", "") or "fingerprint"
        result = {
            "job_id": job_id,
            "status": "completed",
            "filename": safe_filename,
            "input_mode": input_mode,
            "images": {name: f"/api/v1/fingerprint/image/{job_id}/{name}" for name in images},
            "metadata": {**quality, "processing_time_ms": round((time.perf_counter() - started) * 1000, 2)},
        }
        (job_dir / "result.json").write_text(json.dumps(result), encoding="utf-8")
        return result


fingerprint_service = FingerprintService()
