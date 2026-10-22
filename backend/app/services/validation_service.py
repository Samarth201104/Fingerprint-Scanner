import cv2
import numpy as np


def inspect_quality(gray: np.ndarray) -> dict:
    height, width = gray.shape[:2]
    laplacian = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    contrast = float(gray.std())
    brightness = float(gray.mean())
    warnings = []
    if min(width, height) < 96:
        warnings.append("Image is small; ridge detail may be limited.")
    if laplacian < 8:
        warnings.append("Image appears soft or out of focus.")
    if contrast < 12:
        warnings.append("Image has low contrast.")
    if brightness < 20 or brightness > 238:
        warnings.append("Image is unusually dark or bright.")
    score = max(0, min(100, round(min(1, laplacian / 120) * 45 + min(1, contrast / 55) * 35 + (20 if 35 <= brightness <= 220 else 8))))
    return {"width": width, "height": height, "quality_score": score, "blur_score": round(laplacian, 2), "contrast": round(contrast, 2), "brightness": round(brightness, 2), "warnings": warnings}
