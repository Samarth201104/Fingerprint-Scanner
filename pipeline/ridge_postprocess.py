import cv2
import numpy as np

def postprocess(binary):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    clean = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, kernel)

    return clean
