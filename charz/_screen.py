from __future__ import annotations

import os
import sys
from enum import Enum, unique, auto
from typing import TypeGuard

from colex import ColorValue, RESET
from charz_core import Scene, Camera, Node, Transform, Vec2i

from ._components._texture import Texture
from ._grouping import Group
from ._annotations import FileLike, Renderable, TextureNode


@unique
class ConsoleCode(str, Enum):
    CLEAR = "\x1b[2J\x1b[H"


@unique
class CursorCode(str, Enum):
    HIDE = "\x1b[?25l"
    SHOW = "\x1b[?25h"


@unique
class ColorChoice(Enum):
    AUTO = auto()
    ALWAYS = auto()
    NEVER = auto()


class ScreenClassProperties(type):
    COLOR_CHOICE_AUTO = ColorChoice.AUTO
    COLOR_CHOICE_ALWAYS = ColorChoice.ALWAYS
    COLOR_CHOICE_NEVER = ColorChoice.NEVER


class Screen(metaclass=ScreenClassProperties):
    stream: FileLike[str] = sys.stdout  # default stream, may be redirected
    # screen texture buffer with (char, color) tuple
    buffer: list[list[tuple[str, ColorValue | None]]]

    def __init__(
        self,
        width: int = 16,
        height: int = 12,
        *,
        auto_resize: bool = False,
        initial_clear: bool = False,
        final_clear: bool = True,
        hide_cursor: bool = True,
        transparency_fill: str = " ",
        color_choice: ColorChoice = ColorChoice.AUTO,
        stream: FileLike[str] | None = None,
        margin_right: int = 1,
        margin_bottom: int = 1,
    ) -> None:
        if len(transparency_fill) != 1:
            raise ValueError(
                f"string length not equal to 1, got {len(transparency_fill) = }"
            )
        self.width = width
        self.height = height
        self.color_choice = color_choice
        if stream is not None:
            self.stream = stream
            # NOTE: uses class variable `Screen.stream` by default
        self.margin_right = margin_right
        self.margin_bottom = margin_bottom
        self._auto_resize = auto_resize
        self.initial_clear = initial_clear
        self.final_clear = final_clear
        self.hide_cursor = hide_cursor
        self._resize_if_necessary()
        self.transparency_fill = transparency_fill
        self.buffer = []
        self.clear()  # for populating the screen buffer

    @staticmethod
    def _is_texture_nodes(nodes: list[Node]) -> TypeGuard[list[TextureNode]]:
        return all(isinstance(node, Texture) for node in nodes)

    def on_startup(self) -> None:
        if self.is_using_ansi():
            if self.initial_clear:
                self.stream.write(ConsoleCode.CLEAR)
                self.stream.flush()
            if self.hide_cursor:
                self.stream.write(CursorCode.HIDE)
                self.stream.flush()

    def on_cleanup(self) -> None:
        if self.hide_cursor and self.is_using_ansi():
            self.stream.write(CursorCode.SHOW)
            self.stream.flush()
        if self.final_clear:
            old_fill = self.transparency_fill
            self.transparency_fill = " "
            self.clear()
            self.show()
            self.transparency_fill = old_fill

    @property
    def auto_resize(self) -> bool:
        return self._auto_resize

    @auto_resize.setter
    def auto_resize(self, state: bool) -> None:
        self._auto_resize = state
        self._resize_if_necessary()

    def _resize_if_necessary(self) -> None:
        # NOTE: does not mutate screen buffer
        if self.auto_resize:
            try:
                fileno = self.stream.fileno()
            except (ValueError, OSError):
                # do not resize if not proper `.stream.fileno()` is available,
                # like `io.StringIO.fileno()`
                return
            try:
                terminal_size = os.get_terminal_size(fileno)
            except (ValueError, OSError):
                return
            self.width = terminal_size.columns - self.margin_right
            self.height = terminal_size.lines - self.margin_bottom

    @property
    def size(self) -> Vec2i:
        return Vec2i(self.width, self.height)

    @size.setter
    def size(self, size: Vec2i) -> None:
        width, height = size
        if not isinstance(width, int):
            raise ValueError(f"width cannot be of type '{type(size)}', expected 'int'")
        if not isinstance(height, int):
            raise ValueError(f"height cannot be of type '{type(size)}', expected 'int'")
        self.width = width
        self.height = height
        self._resize_if_necessary()

    def is_using_ansi(self) -> bool:
        """Returns whether its using ANSI escape and color codes

        Checks first `.color_choice`. Returns `True` if set to `ALWAYS`,
        and `False` if set to `NEVER`. If set to `AUTO`, check whether a `tty` is detected

        Returns:
            bool: ansi use
        """
        if self.color_choice is ColorChoice.ALWAYS:
            return True
        try:
            fileno = self.stream.fileno()
        except (ValueError, OSError):
            is_a_tty = False
        else:
            try:
                is_a_tty = os.isatty(fileno)
            except OSError:
                is_a_tty = False
        # is not a tty or `ColorChoice.NEVER`
        return self.color_choice is ColorChoice.AUTO and is_a_tty

    def get_actual_size(self) -> Vec2i:
        try:
            fileno = self.stream.fileno()
        except (ValueError, OSError):
            return self.size.copy()
        try:
            terminal_size = os.get_terminal_size(fileno)
        except (ValueError, OSError):
            return self.size.copy()
        actual_width = min(self.width, terminal_size.columns - self.margin_right)
        actual_height = min(self.height, terminal_size.lines - self.margin_bottom)
        return Vec2i(actual_width, actual_height)

    def clear(self) -> None:
        self.buffer = [
            # (char, color) group
            [(self.transparency_fill, None) for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def render(self, node: Renderable, /) -> None:  # noqa: C901
        if not node.is_globally_visible():  # skip if node is invisible
            return
        # TODO: remove this block, as it no longer serves a purpouse
        # current camera should never be None or other class than 'Camera',
        # or subclass of it
        if Camera.current is None or not isinstance(Camera.current, Camera):
            raise TypeError(
                "'Camera.current' cannot be of type "
                f"'{type(Camera.current)}' while rendering"
            )

        color: ColorValue | None = getattr(node, "color")  # noqa: B009
        # TODO: implement rotation when rendering
        # node_global_rotation = node.global_rotation
        node_global_position = node.global_position

        # determine whether to use use the parent of current camera
        # or its parent as anchor for viewport
        anchor = Camera.current
        if (
            not Camera.current.top_level
            and Camera.current.parent is not None
            and isinstance(Camera.current.parent, Transform)
        ):
            anchor = Camera.current.parent
        relative_position = node_global_position - anchor.global_position

        if Camera.current.mode & Camera.MODE_CENTERED:
            relative_position += self.size / 2

        # include half size of camera parent when including size
        viewport_global_position = Camera.current.global_position
        if (
            Camera.current.mode & Camera.MODE_INCLUDE_SIZE
            and Camera.current.parent is not None
            and isinstance(Camera.current.parent, Texture)
        ):
            # adds half of camera's parent's texture size
            # TODO: cache `.parent.texture_size` for the whole iteration in main loop
            viewport_global_position += Camera.current.parent.texture_size / 2

        actual_size = self.get_actual_size()

        texture_size = node.texture_size  # store as variable for performance
        x = int(relative_position.x)
        y = int(relative_position.y)
        if node.centered:
            x = int(relative_position.x - (texture_size.x / 2))
            y = int(relative_position.y - (texture_size.y / 2))

        # TODO: consider nodes with rotation
        # out of bounds
        if x + texture_size.x < 0 or x > actual_size.x:
            return
        if y + texture_size.y < 0 or y > actual_size.y:
            return

        for y_offset, line in enumerate(node.texture):
            y_final = y + y_offset
            for x_offset, char in enumerate(line):
                if char == node.transparency:  # skip transparent char
                    continue
                x_final = x + x_offset
                # insert char into screen buffer if visible
                if 0 <= x_final < actual_size.x and 0 <= y_final < actual_size.y:
                    self.buffer[y_final][x_final] = (char, color)
        # TODO: implement render with rotation

    def show(self) -> None:
        actual_size = self.get_actual_size()
        # construct frame
        out = ""
        is_using_ansi = self.is_using_ansi()
        for lino, row in enumerate(self.buffer[: actual_size.y], start=1):
            for char, color in row[: actual_size.x]:
                if is_using_ansi:
                    if color is None:
                        out += RESET + char
                    else:
                        out += RESET + color + char
                else:
                    out += char
            if lino != actual_size.y:  # not at end
                out += "\n"
        if is_using_ansi:
            out += RESET
            cursor_move_code = f"\x1b[{actual_size.y - 1}A" + "\r"
            out += cursor_move_code
        # write and flush
        self.stream.write(out)
        self.stream.flush()

    def refresh(self) -> None:
        self._resize_if_necessary()
        self.clear()

        # NOTE: `list` is faster than `tuple`, when copying
        texture_nodes = list(Scene.current.groups[Group.TEXTURE].values())
        assert self._is_texture_nodes(
            texture_nodes
        ), f"Node in group '{Group.TEXTURE}' missing 'Texture' component"
        sorted_by_z_index = sorted(texture_nodes, key=lambda node: node.z_index)
        for texture_node in sorted_by_z_index:
            self.render(texture_node)
        self.show()
