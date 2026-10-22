import cv2
import numpy as np

from backend.pipeline.gabor_enhancement import gabor_enhance
from backend.pipeline.preprocessing import preprocess
from backend.pipeline.ridge_postprocess import postprocess
from backend.pipeline.roi_extraction import extract_roi
from backend.pipeline.thresholding import adaptive_threshold


def sample_image():
    image = np.full((240, 240, 3), 220, dtype=np.uint8)
    for y in range(35, 205, 8):
        cv2.ellipse(image, (120, 120), (45, y // 3), 0, 0, 360, (45, 45, 45), 2)
    return image


def test_pipeline_stages_return_valid_images():
    roi = extract_roi(sample_image())
    gray, normalized = preprocess(roi)
    enhanced = gabor_enhance(normalized)
    binary = adaptive_threshold(enhanced)
    final = postprocess(binary)
    assert roi.size and gray.shape == normalized.shape
    assert enhanced.shape == binary.shape == final.shape
    assert set(np.unique(final)).issubset({0, 255})


def test_roi_falls_back_to_full_image_without_contours():
    image = np.zeros((80, 80, 3), dtype=np.uint8)
    assert extract_roi(image).shape == image.shape
