from dataclasses import dataclass


@dataclass(slots=True)
class Hand:
    handedness: str
    landmarks: list[tuple[int, int]]
