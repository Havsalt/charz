from __future__ import annotations

import os
import sys
from math import cos, sin, floor
from enum import Enum, unique, auto
from typing import Iterable

from colex import ColorValue, RESET
from charz_core import Scene, Camera, TransformComponent, Vec2i

from . import text
from ._components._texture import TextureComponent
from ._grouping import Group
from ._annotations import TextureNode, FileLike, Renderable, Char


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
    """Workaround to add class properties to a `AssetLoader`."""

    COLOR_CHOICE_AUTO = ColorChoice.AUTO
    COLOR_CHOICE_ALWAYS = ColorChoice.ALWAYS
    COLOR_CHOICE_NEVER = ColorChoice.NEVER


class Screen(metaclass=ScreenClassProperties):
    """`Screen` class, representing a virtual screen for rendering `ASCII` frames.

    An instance of `Screen` is used by the active `Engine`,
    which is set like this:
    >>> from charz import Engine, Screen
    >>> class MyGame(Engine):
    ...     screen = Screen(
    ...         width=80,
    ...         height=24,
    ...         color_choice=Screen.COLOR_CHOICE_AUTO,
    ...     )
    """

    stream: FileLike[str] = sys.stdout  # Default stream, may be redirected
    # Screen texture buffer with (char, color) tuple
    buffer: list[list[tuple[Char, ColorValue | None]]]

    def __init__(
        self,
        width: int = 16,
        height: int = 12,
        *,
        auto_resize: bool = False,
        initial_clear: bool = True,
        final_clear: bool = True,
        hide_cursor: bool = True,
        transparency_fill: str = " ",
        color_choice: ColorChoice = ColorChoice.AUTO,
        stream: FileLike[str] | None = None,
        margin_right: int = 1,
        margin_bottom: int = 1,
    ) -> None:
        """Initialize screen with given width and height.

        Args:
            width (int): Width of the screen in characters.
            height (int): Height of the screen in characters.
            auto_resize (bool): Whether to automatically resize the screen
                based on terminal size. Defaults to `False`.
            initial_clear (bool): Whether to clear the screen on startup.
                Defaults to `True`.
            final_clear (bool): Whether to clear the screen on cleanup.
                Defaults to `True`.
            hide_cursor (bool): Whether to hide the cursor on startup.
                Defaults to `True`.
            transparency_fill (str): Character used for transparent pixels.
                Defaults to a single space character.
            color_choice (ColorChoice): How colors are handled, defaults to `AUTO`.
            stream (FileLike[str] | None): Output stream, defaults to `sys.stdout`.
            margin_right (int): Right margin in characters, defaults to 1.
            margin_bottom (int): Bottom margin in characters, defaults to 1.
        """
        if len(transparency_fill) != 1:
            raise ValueError(
                f"String length not equal to 1, got {len(transparency_fill) = }"
            )
        self.width = width
        self.height = height
        self.color_choice = color_choice
        if stream is not None:
            self.stream = stream
            # NOTE: Uses class variable `Screen.stream` by default
        self.margin_right = margin_right
        self.margin_bottom = margin_bottom
        self._auto_resize = auto_resize
        self.initial_clear = initial_clear
        self.final_clear = final_clear
        self.hide_cursor = hide_cursor
        self._resize_if_necessary()
        self.transparency_fill = transparency_fill
        self.buffer = []
        self.clear()  # For populating the screen buffer

    def on_startup(self) -> None:
        """Startup hook.

        Called when the screen is being activated.
        The logic is seperated into this method,
        as only 1 screen (which normally uses `stdout`) can be active at a time.
        Multiple screens can be used at the same time,
        as long as they use a different type of filehandle (like sockets or files),
        though this is not recommended.
        """
        if self.is_using_ansi():
            if self.initial_clear:
                self.stream.write(ConsoleCode.CLEAR)
                self.stream.flush()
            if self.hide_cursor:
                self.stream.write(CursorCode.HIDE)
                self.stream.flush()

    def on_cleanup(self) -> None:
        """Cleanup hook.

        Called when the screen is being deactivated.
        The logic is seperated into this method,
        as only 1 screen (which normally uses `stdout`) can be active at a time.
        """
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
        """Whether the screen automatically resizes based on terminal size.

        Returns:
            bool: `True` if auto-resizing is enabled, `False` otherwise.
        """
        return self._auto_resize

    @auto_resize.setter
    def auto_resize(self, state: bool) -> None:
        """Set whether the screen should automatically resize based on terminal size.

        Args:
            state (bool): `True` to enable auto-resizing, `False` to disable.
        """
        self._auto_resize = state
        self._resize_if_necessary()

    def _resize_if_necessary(self) -> None:
        """Resize the screen if requirements are met or circumstances have changed.

        This method checks if the screen should be resized based on the
        `auto_resize` property and the current terminal size.
        If `auto_resize` is `True`, it attempts to get the terminal size
        using `os.get_terminal_size(...)`.
        If successful, it updates the screen dimensions accordingly.

        `NOTE` Does not mutate screen `buffer`.
        """
        if self.auto_resize:
            try:
                fileno = self.stream.fileno()
            except (ValueError, OSError):
                # Do not resize if not proper `.stream.fileno()` is available,
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
        """Get the size of the screen as a `Vec2i`.

        Returns:
            Vec2i: Width and height of the screen, represented by a `Vec2i`.
        """
        return Vec2i(self.width, self.height)

    @size.setter
    def size(self, size: Vec2i) -> None:
        """Set the size of the screen.

        Args:
            size (Vec2i): Width and height, represented by a `Vec2i`.

        Raises:
            ValueError: If the size `Vec2i` could not be unpacked into `2`x`int`.
        """
        width, height = size
        if not isinstance(width, int):
            raise ValueError(f"Width cannot be of type '{type(size)}', expected 'int'")
        if not isinstance(height, int):
            raise ValueError(f"Height cannot be of type '{type(size)}', expected 'int'")
        self.width = width
        self.height = height
        self._resize_if_necessary()

    def is_using_ansi(self) -> bool:
        """Return whether its using ANSI escape and color codes.

        Checks first `.color_choice`. Returns `True` if set to `ALWAYS`,
        and `False` if set to `NEVER`.
        If set to `AUTO`, check whether a `tty` is detected.

        Returns:
            bool: `True` if using ANSI codes, `False` otherwise.
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
        # Returns `False` if not a TTY or is `ColorChoice.NEVER`
        return self.color_choice is ColorChoice.AUTO and is_a_tty

    def get_actual_size(self) -> Vec2i:
        """Get the actual size of the screen based on terminal size.

        The `width` and `height` of the screen are just theoretical maximums,
        though the real terminal might be smaller than these values.
        It also takes into account the right and bottom margins,
        which are nice if jittering occurs because of not accurate values
        reported by `os.get_terminal_size(...)`.
        If `stream` is not set to `stdout`, it will return `width` and `height`.

        Returns:
            Vec2i: Actual size of the screen, adjusted for terminal size and margins.
        """
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
        """Clear the screen `buffer`.

        It will fill the buffer with the transparency fill character,
        as well as `None` for the color, per "pixel".
        """
        self.buffer = [
            # Pair structure: (char, color)
            [(self.transparency_fill, None) for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def render_all(self, nodes: Iterable[Renderable], /) -> None:
        """Render all nodes provided to the screen buffer.

        Args:
            nodes (Iterable[Renderable]): Iterable of nodes with `TextureComponent`.
        """
        nodes_sorted_by_z_index = sorted(nodes, key=lambda node: node.z_index)

        # Include half size of camera parent when including size
        viewport_global_position = Camera.current.global_position

        if Camera.current.mode & Camera.MODE_INCLUDE_SIZE and isinstance(
            Camera.current.parent, TextureComponent
        ):
            # Adds half of camera's parent's texture size
            viewport_global_position += Camera.current.parent.get_texture_size() / 2

        # Determine whether to use use the parent of current camera
        # or its parent as anchor for viewport
        anchor = Camera.current
        if not Camera.current.top_level and isinstance(
            Camera.current.parent, TransformComponent
        ):
            anchor = Camera.current.parent

        for node in nodes_sorted_by_z_index:
            if not node.is_globally_visible():
                continue

            # Cache and lookup node properties/attributes
            node_global_position = node.global_position
            node_global_rotation = node.global_rotation
            node_color: ColorValue | None = getattr(node, "color")  # noqa: B009

            relative_position = node_global_position - anchor.global_position

            if Camera.current.mode & Camera.MODE_CENTERED:
                relative_position.x += self.width / 2
                relative_position.y += self.height / 2

            # Offset from centering
            offset_x = 0
            offset_y = 0
            if node.centered:
                node_texture_size = node.get_texture_size()
                offset_x = node_texture_size.x / 2
                offset_y = node_texture_size.y / 2

            # TODO: Improve performance by using simpler solution when no rotation
            #     - Iterate over each cell, for each row
            for h, row in enumerate(node.texture):
                for w, char in enumerate(row):
                    if char == node.transparency:
                        continue

                    # Adjust starting point based on centering
                    x_diff = w - offset_x
                    y_diff = h - offset_y

                    # Apply rotation using upper-left as the origin
                    # NOTE: `-node_global_rotation` means counter clockwise
                    # Cache using variable
                    neg_node_global_rotation = -node_global_rotation
                    rotated_x = (
                        cos(neg_node_global_rotation) * x_diff
                        - sin(neg_node_global_rotation) * y_diff
                    )
                    rotated_y = (
                        sin(neg_node_global_rotation) * x_diff
                        + cos(neg_node_global_rotation) * y_diff
                    )

                    # Translate to final screen position
                    final_x = relative_position.x + rotated_x
                    final_y = relative_position.y + rotated_y

                    # Apply horizontal index snap
                    char_index = floor(final_x)
                    # Do horizontal boundary check
                    if char_index < 0 or char_index >= self.width:
                        continue

                    # Apply vertical index snap
                    row_index = floor(final_y)
                    if row_index < 0 or row_index >= self.height:
                        continue

                    # Insert rotated char into screen buffer
                    rotated_char = text.rotate(char, node_global_rotation)
                    self.buffer[row_index][char_index] = (rotated_char, node_color)

    def show(self) -> None:
        """Show contents of screen buffer.

        This will print the formatted frame to the screen,
        if `stream` is set to `stdout`.
        """
        actual_size = self.get_actual_size()
        # Construct frame from screen buffer
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
            if lino != actual_size.y:  # Not at end
                out += "\n"
        if is_using_ansi:
            out += RESET
            cursor_move_code = f"\x1b[{actual_size.y - 1}A" + "\r"
            out += cursor_move_code
        # Write and flush
        self.stream.write(out)
        self.stream.flush()

    def refresh(self) -> None:
        """Refresh the screen, by performing multiple steps.

        The steps are:
        1. Resize the screen if necessary.
        2. Clear the screen buffer.
        3. Render all texture nodes in the current scene.
        4. Show the rendered content on the screen.
        """
        self._resize_if_necessary()
        self.clear()
        # NOTE: Uses underlying `list` because it's faster than `tuple` when copying
        texture_nodes = Scene.current.get_group_members(
            Group.TEXTURE,
            type_hint=TextureNode,
        )
        self.render_all(texture_nodes)
        self.show()
