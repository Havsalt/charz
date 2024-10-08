from __future__ import annotations as _annotations

from typing import (
    Any as _Any,
    cast as _cast,
)

from colex import ColorValue as _ColorValue
from typing_extensions import Self as _Self

from .._annotations import (
    NodeType as _NodeType,
    ColorNode as _ColorNode,
)


class Color:  # Component (mixin class)
    color_instances: dict[int, _ColorNode] = {}

    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs)  # type: _ColorNode  # type: ignore
        Color.color_instances[instance.uid] = instance
        return instance  # type: ignore

    color: _ColorValue | None = None

    def with_color(self, color: _ColorValue | None, /) -> _Self:
        self.color = color
        return self

    def free(self) -> None:
        self = _cast(_ColorNode, self)
        del Color.color_instances[self.uid]
        super().free()  # type: ignore
