from __future__ import annotations as _annotations

import os as _os
import sys as _sys

from linflex import Vec2i as _Vec2i
from colex import (
    ColorValue as _ColorValue,
    RESET as _RESET
)

from ._camera import Camera
from ._texture import Texture as _Texture
from ._annotations import (
    FileLike as _FileLike,
    Renderable as _Renderable
)


class Screen:
    stream: _FileLike[str] = _sys.stdout

    def __init__(self, width: int = 16, height: int = 12) -> None:
        self.width = width
        self.height = height
        self._buffer: list[list[tuple[str, _ColorValue | None]]] = []
    
    @property
    def size(self) -> _Vec2i:
        return _Vec2i(self.width, self.height)
    
    @size.setter
    def size(self, value: _Vec2i) -> None:
        width, height = value.to_tuple()
        if any(isinstance(axis, int) for axis in (width, height)):
            raise ValueError(f"value '{value}' requires all axes to be of type 'int'")
        self.width = width
        self.height = height
    
    def clear(self) -> None:
        self._buffer = [
            [(" ", None) for _ in range(self.width)] # (char, color) group
            for _ in range(self.height)
        ]

    def render(self, node: _Renderable) -> None:
        color: _ColorValue | None = getattr(node, "color", None)
        pos = node.global_position
        rel_pos = pos - Camera.current.global_position
        x, y = map(int, rel_pos.to_tuple())
        size = _os.get_terminal_size()
        actual_width = min(self.width, size.columns - 1)
        actual_height = min(self.height, size.lines - 1)
        for y_offset, texture_line in enumerate(node.texture):
            y_final = y + y_offset
            if y_final < 0:
                continue
            if y_final >= actual_height:
                break
            for x_offset, char in enumerate(texture_line):
                x_final = x + x_offset
                if x_final < 0:
                    continue
                if x_final >= actual_width:
                    break
                self._buffer[y_final][x_final] = (char, color)
    
    def show(self) -> None:
        size = _os.get_terminal_size()
        actual_width = min(self.width, size.columns - 1) # -1 is margin
        actual_height = min(self.height, size.lines - 1)
        out = ""
        # move cursor
        if actual_height > 0:
            move_code = f"\u001b[{actual_height}A" + "\r"
            out += move_code
        # construct frame
        for lino, row in enumerate(self._buffer[:actual_height], start=1):
            for char, color in row[:actual_width]:
                if color is not None:
                    out += color + char
                else:
                    out += _RESET + char
            if lino != len(self._buffer): # not at end
                out += "\n"
        out += _RESET
        # write and flush
        self.stream.write(out)
        self.stream.flush()
    
    def refresh(self) -> None:
        self.clear()
        for node in _Texture.iter_texture_nodes():
            self.render(node)
        self.show()
