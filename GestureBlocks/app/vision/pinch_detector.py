from __future__ import annotations

from math import hypot

from app.vision.models import Hand


def pinch_distance(hand: Hand) -> float:
    thumb = hand.landmarks[4]
    index = hand.landmarks[8]

    return hypot(
        thumb[0] - index[0],
        thumb[1] - index[1],
    )

def is_pinching(
    hand: Hand,
    threshold: float = 35,
) -> bool:
    return pinch_distance(hand) < threshold

def pinch_center(
    hand: Hand,
) -> tuple[int, int]:
    thumb = hand.landmarks[4]
    index = hand.landmarks[8]

    return (
        (thumb[0] + index[0]) // 2,
        (thumb[1] + index[1]) // 2,
    )

