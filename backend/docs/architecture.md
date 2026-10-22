# Architecture

The browser frontend owns file selection and camera acquisition. It sends captured or uploaded image bytes as multipart form data to FastAPI. Routes perform transport validation, then delegate to a reusable `FingerprintService`. The service calls the `backend/pipeline/` stages in sequence and stores artifacts under a random job ID. `backend/cli.py` also calls that same service for CLI use.

```mermaid
flowchart LR
  UI[Next.js App Router] -->|multipart HTTP| API[FastAPI routes]
  API --> S[FingerprintService]
  CLI[Python CLI] --> S
  S --> V[Quality metrics / decode]
  V --> P[Existing OpenCV pipeline]
  P --> J[(backend/data/jobs/{job_id})]
  API --> R[Structured JSON / downloads]
  R --> UI
```

Routes are in `backend/app/api/routes`; shared service logic is in `backend/app/services`; Pydantic response shape is in `backend/app/schemas`. Browser camera permissions are requested only by the camera route using `getUserMedia`.

Runtime outputs and uploaded fingerprint data are ignored by Git. There is no authentication, database, or automatic job expiration in this local development release.
