from __future__ import annotations as _annotations

from typing import (
    Generator as _Generator,
    Any as _Any,
)

from colex import ColorValue as _ColorValue

from ._annotations import (
    NodeType as _NodeType,
    ColorNode as _ColorNode,
)


class Color:
    _color_instances: dict[int, _ColorNode] = {}

    @classmethod
    def iter_color_nodes(cls) -> _Generator[_ColorNode, None, None]:
        yield from cls._color_instances.values()

    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs)  # type: _ColorNode  # type: ignore[reportAssignmentType]
        Color._color_instances[instance.uid] = instance
        return instance  # type: ignore

    color: _ColorValue | None = None

    def with_color(self, color: _ColorValue | None, /):
        self.color = color
        return self

    def free(self: _ColorNode) -> None:
        del Color._color_instances[self.uid]
        super().free()
