from __future__ import annotations

from typing import TypeAlias

import cv2

from app.camera.camera import Camera
from app.utils.fps import FPSCounter

from app.vision.models import Hand
from app.vision.hand_tracker import HandTracker
from app.vision.gesture_recognizer import recognize

from app.vision.pinch_detector import (
    is_pinching,
    pinch_center,
)

from app.world.block_manager import BlockManager


Color: TypeAlias = tuple[int, int, int]


# OpenCV uses BGR colors
GREEN: Color = (0, 255, 0)
YELLOW: Color = (255, 255, 0)
ORANGE: Color = (0, 200, 255)


def draw_text(
    frame: cv2.Mat,
    text: str,
    position: tuple[int, int],
    color: Color,
) -> None:

    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2,
    )


def draw_gesture_labels(
    frame: cv2.Mat,
    hands: list[Hand],
) -> None:

    y = 120

    for hand in hands:

        gesture = recognize(hand)

        draw_text(
            frame,
            f"{hand.handedness}: {gesture.value}",
            (20, y),
            ORANGE,
        )

        y += 40


def draw_pinch_indicators(
    frame: cv2.Mat,
    hands: list[Hand],
) -> None:

    for hand in hands:

        if is_pinching(hand):

            center = pinch_center(hand)

            cv2.circle(
                frame,
                center,
                10,
                GREEN,
                -1,
            )


def draw_overlay(
    frame: cv2.Mat,
    fps: float,
    hand_count: int,
) -> None:

    draw_text(
        frame,
        f"FPS: {fps:.1f}",
        (20, 40),
        GREEN,
    )

    draw_text(
        frame,
        f"Hands: {hand_count}",
        (20, 80),
        YELLOW,
    )


def main() -> None:

    camera = Camera()
    tracker = HandTracker()
    fps_counter = FPSCounter()

    # World system
    block_manager = BlockManager()

    try:
        while True:

            frame = camera.read()

            if frame is None:
                continue

            # Mirror webcam
            frame = cv2.flip(frame, 1)

            # Vision system
            hands, results = tracker.process(frame)

            tracker.draw(
                frame,
                results,
            )

            # -------------------------
            # Block interaction
            # -------------------------

            if hands:

                for hand in hands:

                    if is_pinching(hand):

                        center = pinch_center(hand)

                        block_manager.pick(center)
                        block_manager.move_selected(center)

                    else:
                        block_manager.release()

            else:
                block_manager.release()

            # -------------------------
            # Draw world
            # -------------------------

            block_manager.draw(frame)

            # UI
            fps = fps_counter.update()

            draw_overlay(
                frame,
                fps,
                len(hands),
            )

            draw_gesture_labels(
                frame,
                hands,
            )

            draw_pinch_indicators(
                frame,
                hands,
            )

            cv2.imshow(
                "GestureBlocks",
                frame,
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        tracker.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
