from __future__ import annotations

import charz_core
from charz_core import Node, Vec2
from colex import ColorValue

from .._components.texture import TextureComponent
from .._components.color import ColorComponent
from .._annotations import Char


class Sprite(ColorComponent, TextureComponent, charz_core.Node2D):
    r"""`Sprite` node to represent a 2D sprite with texture and color.

    This is the base class for every node that has a texture and color in 2D space.
    Most of the visual nodes will inherit from this class.

    Example:

    Subclassing `Sprite` and overriding class attributes to customize look:

    ```python
    import colex
    from charz import Sprite

    class CustomSprite(Sprite):
        color = colex.RED
        transparency = " "
        centered = True
        texture = [
            "  O",
            "/ | \\",
            " / \\",
        ]
    ```
    """

    def __init__(
        self,
        parent: Node | None = None,
        *,
        position: Vec2 | None = None,
        rotation: float | None = None,
        top_level: bool | None = None,
        texture: list[str] | None = None,
        visible: bool | None = None,
        centered: bool | None = None,
        z_index: int | None = None,
        transparency: Char | None = None,
        color: ColorValue | None = None,
    ) -> None:
        charz_core.Node2D.__init__(
            self,
            parent=parent,
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

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + f"#{self.uid}"
            + f":{round(self.position, 2)}"
            + f":{round(self.rotation, 2)}R"
            + f":{'{}x{}'.format(*self.get_texture_size())}"
            + f":{repr(self.color)}"
            + ")"
        )
