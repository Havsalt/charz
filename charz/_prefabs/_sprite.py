from __future__ import annotations

from colex import ColorValue
from linflex import Vec2

from .._node import Node
from .._components._transform import Transform
from .._components._texture import Texture
from .._components._color import Color


class Sprite(Color, Texture, Transform, Node):
    def __init__(
        self,
        parent: Node | None = None,
        *,
        process_priority: int | None = None,
        position: Vec2 | None = None,
        rotation: float | None = None,
        top_level: bool | None = None,
        texture: list[str] | None = None,
        visible: bool | None = None,
        centered: bool | None = None,
        z_index: int | None = None,
        transparency: str | None = None,
        color: ColorValue | None = None,
    ) -> None:
        if parent is not None:
            self.parent = parent
        if process_priority is not None:
            self.process_priority = process_priority
        if position is not None:
            self.position = position
        if rotation is not None:
            self.rotation = rotation
        if top_level is not None:
            self.top_level = top_level
        if texture is not None:
            self.texture = texture
        if visible is not None:
            self.visible = visible
        if centered is not None:
            self.centered = centered
        if z_index is not None:
            self.z_index = z_index
        if transparency is not None:
            self.transparency = transparency
        if color is not None:
            self.color = color

    def __str__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + f"#{self.uid}"
            + f":{self.position}"
            + f":{round(self.rotation, 2)}R"
            + f":{'{}x{}'.format(*self.texture_size.to_tuple())}"
            + f":{repr(self.color)}"
            + ")"
        )
