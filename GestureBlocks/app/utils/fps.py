from __future__ import annotations

import time


class FPSCounter:
    """Simple FPS counter."""

    def __init__(self):
        self.previous_time = time.perf_counter()

    def update(self) -> float:
        current = time.perf_counter()

        fps = 1.0 / (current - self.previous_time)

        self.previous_time = current

        return fps