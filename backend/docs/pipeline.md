# Fingerprint pipeline

The implementation retains the repository's existing CV stages and routes each input mode through the same service:

1. Decode image bytes with OpenCV and reject undecodable data.
2. Measure source dimensions, Laplacian blur variance, contrast, brightness, and a heuristic 0–100 score.
3. `extract_roi`: convert to grayscale, blur, Otsu threshold, close gaps, then crop the largest external contour. If no contour exists, use the whole image.
4. `preprocess`: grayscale, Gaussian blur, CLAHE normalization.
5. `gabor_enhance`: compute absolute responses for 16 orientations, average, normalize, bilateral smooth.
6. `adaptive_threshold`: Gaussian adaptive thresholding.
7. `postprocess`: morphological opening and closing.

Intermediate arrays are written to `backend/data/jobs/{job_id}` and exposed through local image endpoints for the UI. The pipeline performs enhancement only: it does not claim fingerprint identity matching or certified sensor acquisition.
