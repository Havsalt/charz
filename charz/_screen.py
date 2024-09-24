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
    stream: _FileLike[str] = _sys.stdout  # default stream, may be redirected
    # screen texture buffer with (char, color) tuple
    buffer: list[list[tuple[str, _ColorValue | None]]]

    def __init__(
        self,
        width: int = 16,
        height: int = 12,
        auto_resize: bool = False,
        transparancy_fill: str = " ",
    ) -> None:
        self.width = width
        self.height = height
        self._auto_resize = auto_resize
        self._resize_if_necessary()
        self.transparancy_fill = transparancy_fill
        self.buffer = []
        self.clear()  # for populating the list with an empty screen

    @property
    def auto_resize(self) -> bool:
        return self._auto_resize

    @auto_resize.setter
    def auto_resize(self, state: bool) -> None:
        self._auto_resize = state
        self._resize_if_necessary()

    def _resize_if_necessary(self) -> None:  # NOTE: does not mutate screen buffer
        if self.auto_resize:
            terminal_size = _os.get_terminal_size(self.stream.fileno())
            self.width = terminal_size.columns - 1
            self.height = terminal_size.lines - 1

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

    def with_auto_resize(self, state: bool = True, /):
        self.auto_resize = state
        return self

    def with_transparancy_fill(self, fill_char: str, /):
        if len(fill_char) != 1:
            raise ValueError(
                "'transparancy_fill' cannot be a 'str' with length other than 1,"
                f"got length {len(fill_char)}"
            )
        self.transparancy_fill = fill_char
        return self

    @property
    def size(self) -> _Vec2i:
        return _Vec2i(self.width, self.height)

    @size.setter
    def size(self, value: _Vec2i) -> None:
        width, height = value.to_tuple()
        if not isinstance(width, int):
            raise ValueError(f"width cannot be of type '{type(value)}', expected 'int'")
        if not isinstance(height, int):
            raise ValueError(f"height cannot be of type '{type(value)}', expected 'int'")
        self.width = width
        self.height = height
        self._resize_if_necessary()

    def clear(self) -> None:
        self.buffer = [
            # (char, color) group
            [(self.transparancy_fill, None) for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def render(self, node: _Renderable, /) -> None:  # noqa: C901
        if not node.is_globally_visible():  # skip if node is invisible
            return
        # current camera should never be None or other class than 'Camera',
        # or subclass of it
        if _Camera.current is None or not isinstance(_Camera.current, _Camera):
            raise TypeError(
                "'Camera.current' cannot be of type "
                f"'{type(_Camera.current)}' while rendering"
            )

        color: _ColorValue | None = getattr(node, "color")  # noqa: B009
        # TODO: implement rotation when rendering
        # node_global_rotation = node.global_rotation
        node_global_position = node.global_position

        # determine whether to use use the parent of current camera
        # or its parent as anchor for viewport
        anchor = _Camera.current
        if _Camera.current.parent is not None and isinstance(
            _Camera.current.parent, _Transform
        ):
            anchor = _Camera.current.parent
        relative_position = node_global_position - anchor.global_position

        if _Camera.current.mode & _CameraMode.CENTERED:
            relative_position += self.size / 2

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
                if char == node.transparency:  # skip transparent char
                    continue
                x_final = x + x_offset
                # insert char into screen buffer if visible
                if 0 <= x_final < actual_width and 0 <= y_final < actual_height:
                    self.buffer[y_final][x_final] = (char, color)
        # TODO: implement render with rotation

    def show(self) -> None:
        # TODO: use better ANSI control codes to clear the screen better
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
        self._resize_if_necessary()
        self.clear()
        for node in sorted(  # NOTE: iterator becomes a 'list'
            # NOTE: 'list' is faster than 'tuple', when copying
            list(_Texture.texture_instances.values()),  # iterate a copy
            key=lambda node: node.z_index,
        ):
            self.render(node)
        self.show()
