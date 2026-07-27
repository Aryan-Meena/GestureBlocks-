from __future__ import annotations

from app.vision.models import Hand


FINGER_TIPS = (4, 8, 12, 16, 20)

def fingers_up(hand: Hand) -> list[bool]:
    points = hand.landmarks

    if hand.handedness == "Right":
        thumb = points[4][0] > points[3][0]
    else:
        thumb = points[4][0] < points[3][0]

    index = points[8][1] < points[6][1]
    middle = points[12][1] < points[10][1]
    ring = points[16][1] < points[14][1]
    pinky = points[20][1] < points[18][1]

    return [
        thumb,
        index,
        middle,
        ring,
        pinky,
    ]