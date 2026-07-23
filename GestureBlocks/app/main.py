from __future__ import annotations

import cv2

from camera.camera import Camera
from utils.fps import FPSCounter
from vision.hand_tracker import HandTracker


def main() -> None:
    camera = Camera()

    tracker = HandTracker()

    fps_counter = FPSCounter()

    try:
        while True:

            frame = camera.read()

            hands = tracker.process(frame)

            fps = fps_counter.update()

            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Hands: {len(hands)}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2,
            )

            cv2.imshow("GestureBlocks", frame)

            key = cv2.waitKey(1)

            if key == ord("q"):
                break

    finally:
        tracker.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()