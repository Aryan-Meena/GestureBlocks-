from enum import Enum

from app.vision.finger_detector import fingers_up
from app.vision.models import Hand

class Gesture(Enum):
    UNKNOWN = "UNKNOWN"
    FIST = "FIST"
    OPEN_PALM = "OPEN_PALM"
    POINT = "POINT"
    PEACE = "PEACE"

def recognize(hand: Hand) -> Gesture:
    fingers = fingers_up(hand)

    if fingers == [False, False, False, False, False]:
        return Gesture.FIST

    if fingers == [True, True, True, True, True]:
        return Gesture.OPEN_PALM

    if fingers == [False, True, False, False, False]:
        return Gesture.POINT

    if fingers == [False, True, True, False, False]:
        return Gesture.PEACE

    return Gesture.UNKNOWN    