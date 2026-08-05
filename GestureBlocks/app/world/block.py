from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

Color = tuple[int, int, int]


@dataclass(slots=True)
class Block:
    x: int
    y: int
    width: int
    height: int
    color: Color
    depth: int = 25
    alpha: float = 0.45
    selected: bool = False

    def draw(self, frame: np.ndarray) -> None:
        """
        Draw a transparent 3D cube.
        """

        overlay = frame.copy()

        x1 = self.x
        y1 = self.y

        x2 = self.x + self.width
        y2 = self.y + self.height

        d = self.depth

        # -----------------------
        # Top face
        # -----------------------

        top_face = np.array(
            [
                (x1, y1),
                (x1 + d, y1 - d),
                (x2 + d, y1 - d),
                (x2, y1),
            ],
            dtype=np.int32,
        )

        cv2.fillPoly(
            overlay,
            [top_face],
            self.light_color(),
        )

        # -----------------------
        # Right face
        # -----------------------

        side_face = np.array(
            [
                (x2, y1),
                (x2 + d, y1 - d),
                (x2 + d, y2 - d),
                (x2, y2),
            ],
            dtype=np.int32,
        )

        cv2.fillPoly(
            overlay,
            [side_face],
            self.dark_color(),
        )

        # -----------------------
        # Front face
        # -----------------------

        cv2.rectangle(
            overlay,
            (x1, y1),
            (x2, y2),
            self.color,
            -1,
        )

        # Blend transparency

        cv2.addWeighted(
            overlay,
            self.alpha,
            frame,
            1 - self.alpha,
            0,
            frame,
        )

        # Selection highlight

        if self.selected:
            cv2.rectangle(
                frame,
                (x1 - 3, y1 - 3),
                (x2 + 3, y2 + 3),
                (0, 255, 255),
                3,
            )

        # Cube outline

        cv2.polylines(
            frame,
            [
                np.array(
                    [
                        (x1, y1),
                        (x1 + d, y1 - d),
                        (x2 + d, y1 - d),
                        (x2, y1),
                        (x2, y2),
                        (x2 + d, y2 - d),
                        (x2 + d, y1 - d),
                    ],
                    dtype=np.int32,
                )
            ],
            False,
            (255, 255, 255),
            2,
        )

    def light_color(self) -> Color:
        """
        Brighter top surface.
        """

        b, g, r = self.color

        return (
            min(b + 60, 255),
            min(g + 60, 255),
            min(r + 60, 255),
        )

    def dark_color(self) -> Color:
        """
        Darker side surface.
        """

        b, g, r = self.color

        return (
            b // 2,
            g // 2,
            r // 2,
        )

    def contains(
        self,
        point: tuple[int, int],
    ) -> bool:
        px, py = point

        return (
            self.x <= px <= self.x + self.width
            and self.y <= py <= self.y + self.height
        )
