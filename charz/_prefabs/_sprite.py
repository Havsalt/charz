from __future__ import annotations

from colex import ColorValue
from charz_core import Node, Node2D, Vec2

from .._components._texture import Texture
from .._components._color import Color


class Sprite(Color, Texture, Node2D):
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
        super().__init__(
            parent=parent,
            process_priority=process_priority,
            position=position,
            rotation=rotation,
            top_level=top_level,
        )
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
            + f":{round(self.position, 2)}"
            + f":{round(self.rotation, 2)}R"
            + f":{'{}x{}'.format(*self.texture_size.to_tuple())}"
            + f":{repr(self.color)}"
            + ")"
        )
