from __future__ import annotations

from typing import List

import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    """Detects and draws MediaPipe hand landmarks."""

    def __init__(
        self,
        max_num_hands: int = 2,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.7,
    ):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def process(self, frame: np.ndarray) -> List[List[tuple[float, float, float]]]:
        """
        Detect hands and return normalized landmark coordinates.

        Returns:
            [
                [(x, y, z), ... 21 landmarks],
                [(x, y, z), ...]
            ]
        """

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        hands = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                )

                landmark_list = []

                for landmark in hand_landmarks.landmark:
                    landmark_list.append(
                        (
                            landmark.x,
                            landmark.y,
                            landmark.z,
                        )
                    )

                hands.append(landmark_list)

        return hands

    def close(self) -> None:
        self.hands.close()