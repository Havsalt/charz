from __future__ import annotations as _annotations

from colex import ColorValue as _ColorValue

from typing import Generator as _Generator


class Color:
    _color_instances: dict[int, Color] = {}

    @classmethod
    def iter_nodes(cls) -> _Generator[Color, None, None]:
        yield from cls._color_instances.values()
    
    color: _ColorValue
