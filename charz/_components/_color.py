from __future__ import annotations

from colex import ColorValue
from charz_core import Self


class ColorComponent:  # Component (mixin class)
    r"""`ColorComponent` mixin class for node.

    Example:

    Setting color of node. Since `Sprite` is composed using
    `ColorComponent`, `TextureComponent` and `Node2D`,
    the easiest will be to use a `Sprite` as a base:

    ```python
    import colex  # Color library used
    from charz import Sprite

    class PurpleMonster(Sprite):
        color = colex.PURPLE
        texture = [
            "   %",
            "~' | '~",
            "  / \\",
        ]
    ```

    Attributes:
        `color`: `ColorValue | None` - Optional color value for the node.
    """

    color: ColorValue | None = None

    def with_color(self, color: ColorValue | None, /) -> Self:
        self.color = color
        return self
