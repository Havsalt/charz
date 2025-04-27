from __future__ import annotations as _annotations

from linflex import Vec2

from .._node import Node
from .._components._transform import Transform


class Node2D(Transform, Node):
    def __init__(
        self,
        parent: Node | None = None,
        *,
        process_priority: int | None = None,
        position: Vec2 | None = None,
        rotation: float | None = None,
        top_level: bool | None = None,
    ) -> None:
        super().__init__(parent=parent)
        if process_priority is not None:
            self.process_priority = process_priority
        if position is not None:
            self.position = position
        if rotation is not None:
            self.rotation = rotation
        if top_level:  # `bool` and `None` check combined
            self.top_level = top_level

    def __str__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + f"#{self.uid}"
            + f":{round(self.position, 2)}"
            + f":{round(self.rotation, 2)}R"
            + ")"
        )
