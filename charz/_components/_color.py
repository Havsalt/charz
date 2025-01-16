from __future__ import annotations

from typing import Any

from colex import ColorValue
from typing_extensions import Self

from .._annotations import ColorNode


class Color:  # Component (mixin class)
    color_instances: dict[int, ColorNode] = {}

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        Color.color_instances[instance.uid] = instance  # type: ignore
        return instance

    color: ColorValue | None = None

    def with_color(self, color: ColorValue | None, /) -> Self:
        self.color = color
        return self

    def _free(self) -> None:
        del Color.color_instances[self.uid]  # type: ignore
        super()._free()  # type: ignore
