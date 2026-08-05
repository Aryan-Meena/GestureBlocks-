from __future__ import annotations

import numpy as np

from app.world.block import Block


class BlockManager:
    def __init__(self) -> None:

        self.blocks = [
            Block(
                x=250,
                y=180,
                width=120,
                height=120,
                color=(255, 200, 100),
                alpha=0.45,
            )
        ]

        self.selected: Block | None = None
        self.grab_offset: tuple[int, int] = (0, 0)

    def pick(
        self,
        point: tuple[int, int],
    ) -> None:

        if self.selected is not None:
            return

        for block in reversed(self.blocks):
            if block.contains(point):

                # Bring selected block to the front
                self.blocks.remove(block)
                self.blocks.append(block)

                self.selected = block

                px, py = point

                self.grab_offset = (
                    px - block.x,
                    py - block.y,
                )

                return

    def move_selected(
        self,
        point: tuple[int, int],
    ) -> None:

        if self.selected is None:
            return

        x, y = point
        offset_x, offset_y = self.grab_offset

        self.selected.x = x - offset_x
        self.selected.y = y - offset_y

    def release(self) -> None:
        self.selected = None
        self.grab_offset = (0, 0)

    def draw(
        self,
        frame: np.ndarray,
    ) -> None:

        for block in self.blocks:
            block.selected = block is self.selected
            block.draw(frame)
