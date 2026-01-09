import cv2
import numpy as np

def gabor_enhance(img):
    img = img.astype(np.float32) / 255.0

    thetas = np.linspace(0, np.pi, 16, endpoint=False)
    responses = []

    for theta in thetas:
        kernel = cv2.getGaborKernel(
            ksize=(31,31),
            sigma=4.0,
            theta=theta,
            lambd=10.0,
            gamma=0.5,
            psi=0,
            ktype=cv2.CV_32F
        )
        resp = cv2.filter2D(img, cv2.CV_32F, kernel)
        responses.append(np.abs(resp))

    energy = np.mean(responses, axis=0)

    # Contrast enhancement
    energy = cv2.normalize(energy, None, 0, 255, cv2.NORM_MINMAX)
    energy = energy.astype(np.uint8)

    # Edge-preserving smoothing
    energy = cv2.bilateralFilter(energy, 9, 50, 50)

    return energy
