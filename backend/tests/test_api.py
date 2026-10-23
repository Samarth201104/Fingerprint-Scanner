import asyncio
import os

import cv2
import httpx
import numpy as np

from backend.app.main import app
from backend.app.services.fingerprint_service import cleanup_expired_jobs


async def _request(method: str, path: str, **kwargs):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.request(method, path, **kwargs)


def request(method: str, path: str, **kwargs):
    return asyncio.run(_request(method, path, **kwargs))


def png_bytes():
    image = np.full((240, 240), 200, dtype=np.uint8)
    for y in range(40, 200, 8):
        cv2.ellipse(image, (120, 120), (45, y // 3), 0, 0, 360, 30, 2)
    return cv2.imencode(".png", image)[1].tobytes()


def test_health_endpoint():
    response = request("GET", "/api/v1/health")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "healthy"


def test_cors_allows_next_dev_server_on_port_3001():
    response = request("GET", "/api/v1/health", headers={"Origin": "http://localhost:3001"})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3001"


def test_expired_job_cleanup_only_removes_old_job_directories(tmp_path):
    expired = tmp_path / ("a" * 32)
    recent = tmp_path / ("b" * 32)
    unrelated = tmp_path / "user-files"
    for directory in (expired, recent, unrelated):
        directory.mkdir()
        (directory / "result.json").write_text("{}", encoding="utf-8")
    old_time = 1_000_000
    os.utime(expired, (old_time, old_time))

    removed = cleanup_expired_jobs(tmp_path, now=old_time + 2 * 60 * 60, ttl_hours=1)

    assert removed == 1
    assert not expired.exists()
    assert recent.exists()
    assert unrelated.exists()


def test_invalid_upload_has_structured_error():
    response = request("POST", "/api/v1/fingerprint/process", files={"file": ("bad.png", b"not an image", "image/png")})
    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "INVALID_IMAGE"


def test_process_and_batch_endpoints():
    payload = png_bytes()
    single = request("POST", "/api/v1/fingerprint/process", files={"file": ("finger.png", payload, "image/png")})
    assert single.status_code == 200
    assert set(single.json()["data"]["images"]) == {"original", "roi", "preprocessed", "enhanced", "binary", "final"}
    job_id = single.json()["data"]["job_id"]
    assert request("GET", f"/api/v1/fingerprint/result/{job_id}").status_code == 200
    assert request("GET", single.json()["data"]["images"]["final"]).status_code == 200
    downloaded = request("GET", f"/api/v1/fingerprint/download/{job_id}/final")
    assert downloaded.status_code == 200
    assert "attachment" in downloaded.headers["content-disposition"]
    batch = request("POST", "/api/v1/fingerprint/process-batch", files=[("files", ("finger.png", payload, "image/png")), ("files", ("bad.jpg", b"bad", "image/jpeg"))])
    assert batch.status_code == 200
    assert batch.json()["data"]["succeeded"] == 1
    assert batch.json()["data"]["failed"] == 1
