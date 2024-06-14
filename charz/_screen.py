from __future__ import annotations as _annotations

from ._node import Node as _Node


class Screen:
    def __init__(self, width: int = 16, height: int = 12) -> None:
        self.width = width
        self.height = height
        self._buffer: list[list[str]] = []
    
    def clear(self) -> None:
        self._buffer = [
            [" " for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def render(self, node: _Node) -> None:
        ...
    
    def refresh(self) -> None:
        ...
