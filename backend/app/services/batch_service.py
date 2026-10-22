from concurrent.futures import ThreadPoolExecutor
from backend.app.services.fingerprint_service import fingerprint_service
from backend.app.core.logging import logger


def process_batch(files: list[tuple[str, bytes]]) -> dict:
    def process(item: tuple[str, bytes]) -> dict:
        filename, content = item
        try:
            result = fingerprint_service.process_bytes(content, filename, "batch")
            logger.info("Batch image succeeded filename=%s job_id=%s", filename, result["job_id"])
            return {"success": True, "result": result}
        except Exception as exc:
            logger.exception("Batch image failed filename=%s", filename)
            return {"success": False, "filename": filename, "error": str(exc)}

    with ThreadPoolExecutor(max_workers=min(4, max(1, len(files)))) as pool:
        results = list(pool.map(process, files))
    return {"total": len(results), "succeeded": sum(bool(item["success"]) for item in results), "failed": sum(not item["success"] for item in results), "results": results}
