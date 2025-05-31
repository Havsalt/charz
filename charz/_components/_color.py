from __future__ import annotations

from colex import ColorValue
from charz_core import Self


class ColorComponent:  # Component (mixin class)
    """`ColorComponent` mixin class for node.

    Attributes:
        `color`: `ColorValue | None` - Optional color value for the node.
    """

    color: ColorValue | None = None

    def with_color(self, color: ColorValue | None, /) -> Self:
        self.color = color
        return self
