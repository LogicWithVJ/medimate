import cv2
import numpy as np


def preprocess_prescription_image(input_path, output_path):
    """
    Preprocesses a prescription image to improve OCR accuracy.

    Steps:
    1. Load the image
    2. Convert to grayscale (removes color noise, OCR works on intensity)
    3. Denoise (reduces camera-sensor noise from phone photos)
    4. Improve contrast using adaptive thresholding
    5. Save the processed image to output_path

    The ORIGINAL file at input_path is never modified — this function
    only reads it and writes a new file at output_path.

    Returns True on success, False if the image could not be read.
    """

    image = cv2.imread(input_path)

    if image is None:
        # File exists but isn't a readable image (corrupted, wrong format, etc.)
        return False

    # Step 1: Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 2: Denoise — removes small speckles/noise while preserving edges (text)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # Step 3: Adaptive thresholding — converts to black/white, adapting to
    # uneven lighting across the image (common in phone photos of paper)
    processed = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31,
        C=15,
    )

    cv2.imwrite(output_path, processed)
    return True