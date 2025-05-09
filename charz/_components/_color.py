from __future__ import annotations

from colex import ColorValue
from charz_core import Self


class ColorComponent:  # Component (mixin class)
    color: ColorValue | None = None

    def with_color(self, color: ColorValue | None, /) -> Self:
        self.color = color
        return self
