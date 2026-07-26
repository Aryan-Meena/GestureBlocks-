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


    def draw(self, frame) -> None:

        for block in self.blocks:
            block.draw(frame)
