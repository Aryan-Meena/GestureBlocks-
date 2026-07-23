from __future__ import annotations

import cv2
import numpy as np


class Camera:
    """Simple wrapper around OpenCV VideoCapture."""

    def __init__(self, camera_index: int = 0, width: int = 1280, height: int = 720):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Unable to open webcam.")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self) -> np.ndarray:
        success, frame = self.cap.read()

        if not success:
            raise RuntimeError("Failed to read frame from webcam.")

        return frame

    def release(self) -> None:
        self.cap.release()