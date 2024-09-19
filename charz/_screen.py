from __future__ import annotations as _annotations

import os as _os
import sys as _sys

from linflex import Vec2i as _Vec2i
from colex import (
    ColorValue as _ColorValue,
    RESET as _RESET,
)

from ._camera import (
    Camera as _Camera,
    CameraMode as _CameraMode,
)
from ._transform import Transform as _Transform
from ._texture import Texture as _Texture
from ._annotations import (
    FileLike as _FileLike,
    Renderable as _Renderable,
)


class Screen:
    stream: _FileLike[str] = _sys.stdout

    def __init__(self, width: int = 16, height: int = 12) -> None:
        self.width = width
        self.height = height
        self.buffer: list[list[tuple[str, _ColorValue | None]]] = []

    def with_stream(self, stream: _FileLike[str], /):
        self.stream = stream
        return self

    def with_width(self, width: int, /):
        self.width = width
        return self

    def with_height(self, height: int, /):
        self.height = height
        return self

    def with_size(self, size: _Vec2i, /):
        self.size = size
        return self

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
        self.buffer = [
            [(" ", None) for _ in range(self.width)]  # (char, color) group
            for _ in range(self.height)
        ]

    def render(self, node: _Renderable, /) -> None:  # noqa: C901
        if _Camera.current is None:  # should never be None
            raise TypeError(
                "'Camera.current' cannot be of type "
                f"'{type(_Camera.current)}' while rendering"
            )

        color: _ColorValue | None = getattr(node, "color")  # noqa: B009
        # node_global_rotation = node.global_rotation # TODO: implement
        node_global_position = node.global_position

        # determine whether to use use the parent of current camera
        # or its parent as anchor for viewport
        anchor = _Camera.current
        if (
            _Camera.current.mode & _CameraMode.FOLLOW
            and _Camera.current.parent is not None
            and isinstance(_Camera.current.parent, _Transform)
        ):
            anchor = _Camera.current.parent
        relative_position = node_global_position - anchor.global_position

        if _Camera.current.mode & _CameraMode.CENTERED:
            relative_position += self.size / 4

        # include half size of camera parent when including size
        viewport_global_position = _Camera.current.global_position
        if (
            _Camera.current.mode & _CameraMode.INCLUDE_SIZE
            and _Camera.current.parent is not None
            and isinstance(_Camera.current.parent, _Texture)
        ):
            # adds half of camera's parent's texture size
            viewport_global_position += _Camera.current.parent.get_texture_size() / 2

        terminal_size = _os.get_terminal_size()
        actual_width = min(self.width, terminal_size.columns - 1)
        actual_height = min(self.height, terminal_size.lines - 1)

        texture_size = node.get_texture_size()
        x = int(relative_position.x)
        y = int(relative_position.y)
        if node.centered:
            x = int(relative_position.x - (texture_size.x / 2))
            y = int(relative_position.y - (texture_size.y / 2))

        # out of bounds
        # TODO: consider nodes with rotation
        if x + texture_size.x < 0 or x > actual_width:
            return
        if y + texture_size.y < 0 or y > actual_height:
            return

        for y_offset, line in enumerate(node.texture):
            y_final = y + y_offset
            for x_offset, char in enumerate(line):
                x_final = x + x_offset
                # insert char into screen buffer if visible
                if 0 <= x_final < actual_width:
                    if 0 <= y_final < actual_height:
                        self.buffer[y_final][x_final] = (char, color)
        # TODO: implement render with rotation

    def show(self) -> None:
        size = _os.get_terminal_size()
        actual_width = min(self.width, size.columns - 1)  # -1 is margin
        actual_height = min(self.height, size.lines - 1)
        out = ""
        # move cursor
        if actual_height > 0:
            move_code = f"\u001b[{actual_height}A" + "\r"
            out += move_code
        # construct frame
        for lino, row in enumerate(self.buffer[:actual_height], start=1):
            for char, color in row[:actual_width]:
                if color is not None:
                    out += color + char
                else:
                    out += _RESET + char
            if lino != len(self.buffer):  # not at end
                out += "\n"
        out += _RESET
        # write and flush
        self.stream.write(out)
        self.stream.flush()

    def refresh(self) -> None:
        self.clear()
        for node in sorted(
            _Texture.iter_texture_nodes(),
            key=lambda node: node.z_index,
        ):
            self.render(node)
        self.show()
