# API reference

Base URL: `http://localhost:8000/api/v1`. Uploads use multipart form data. Successful responses are `{ "success": true, "message": "...", "data": ... }`; errors use `{ "success": false, "message": "...", "error_code": "..." }` (FastAPI places route error bodies under `detail`).

| Method | Path | Input / purpose |
| --- | --- | --- |
| GET | `/health` | Service health |
| POST | `/fingerprint/process` | `file`, optional `input_mode`; returns stages and metadata |
| POST | `/fingerprint/validate` | `file`; returns dimensions and quality indicators |
| POST | `/fingerprint/process-batch` | repeated `files` fields; each file succeeds or fails independently |
| GET | `/fingerprint/result/{job_id}` | Read a saved job result |
| GET | `/fingerprint/image/{job_id}/{stage}` | Inline image for one of the six processing stages |
| GET | `/fingerprint/download/{job_id}/{stage}` | Download one of original, roi, preprocessed, enhanced, binary, final |

Accepted extensions: JPG/JPEG, PNG, BMP, WEBP. Upload limit is 12 MB per image. Batch size is limited to 50. Invalid images return a structured 422 error; unsupported file types return 415.
