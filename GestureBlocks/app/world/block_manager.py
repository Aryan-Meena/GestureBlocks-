from __future__ import annotations

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

        # Currently grabbed block
        self.selected: Block | None = None

    def pick(
        self,
        point: tuple[int, int],
    ) -> None:

        # Already holding something
        if self.selected is not None:
            return

        # Pick top-most block first
        for block in reversed(self.blocks):
            if block.contains(point):
                self.selected = block
                return

    def move_selected(
        self,
        point: tuple[int, int],
    ) -> None:

        if self.selected is None:
            return

        x, y = point

        self.selected.x = x - self.selected.width // 2
        self.selected.y = y - self.selected.height // 2

    def release(self) -> None:
        self.selected = None

    def draw(self, frame) -> None:

        for block in self.blocks:
            block.draw(frame)
