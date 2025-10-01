from __future__ import annotations

from typing import Any, NamedTuple

from colex import ColorValue
from charz_core import Node, Self, Vec2

from .sprite import Sprite
from .._annotations import Char


class Panel(Sprite):
    """`Panel` node for making a pretty frame.

    You can assign a `PanelStyle` to `.style` for customizing the style.

    To have content be rendered above a `<Panel>`, do one of:
        - Content have a greater `z_index` than `<Panel>`
        - Content is created after `<Panel>` instance

    `NOTE` Content **can** be rendered outside the panel,
    so it does **not** cutoff at border.
    """

    style: PanelStyle
    _width: int = 12
    _height: int = 8

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        if (class_style := getattr(instance, "style", None)) is not None:
            instance.style = PanelStyle(**class_style._asdict())
        else:
            instance.style = PanelStyle()
        return instance

    def __init__(
        self,
        parent: Node | None = None,
        *,
        position: Vec2 | None = None,
        rotation: float | None = None,
        top_level: bool | None = None,
        visible: bool | None = None,
        centered: bool | None = None,
        z_index: int | None = None,
        transparency: Char | None = None,
        color: ColorValue | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> None:
        Sprite.__init__(
            self,
            parent=parent,
            position=position,
            rotation=rotation,
            top_level=top_level,
            visible=visible,
            centered=centered,
            z_index=z_index,
            transparency=transparency,
            color=color,
        )
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

    def _update_panel_texture(self) -> None:
        self.texture = [
            self.style.upper_left_corner
            + self.style.top_border * (self._width - 2)
            + self.style.upper_right_corner,
            *[
                self.style.left_border + " " * (self._width - 2) + self.style.right_border
                for _ in range(self._height - 2)
            ],
            self.style.bottom_left_corner
            + self.style.bottom_border * (self._width - 2)
            + self.style.bottom_right_corner,
        ]

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        if value < 2:
            raise ValueError(f"Width must be at least 2, got {value}")
        self._width = value
        self._update_panel_texture()

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        if value < 2:
            raise ValueError(f"Height must be at least 2, got {value}")
        self._height = value
        self._update_panel_texture()


class PanelStyle(NamedTuple):
    """`PanelStyle` used to customize the appearance of a `Panel`.

    Attributes:
        - `upper_left_corner` - `Char`
        - `upper_right_corner` - `Char`
        - `bottom_left_corner` - `Char`
        - `bottom_right_corner` - `Char`
        - `left_border` - `Char`
        - `right_border` - `Char`
        - `top_border` - `Char`
        - `bottom_border` - `Char`

    Example:

    Customizing the appearance of a `Panel` using `PanelStyle`:

    ```python
    from charz import Panel, PanelStyle

    class MyPanel(Panel):
        style = PanelStyle(
            upper_left_corner="╔",
            upper_right_corner="╗",
            bottom_left_corner="╚",
            bottom_right_corner="╝",
            left_border="║",
            right_border="║",
            top_border="═",
            bottom_border="═",
        )
    ```

    ↳ Results in panel looking like:

    ```bash
    ╔════════╗
    ║        ║
    ║        ║
    ╚════════╝
    ```
    """

    upper_left_corner: Char = "+"
    upper_right_corner: Char = "+"
    bottom_left_corner: Char = "+"
    bottom_right_corner: Char = "+"

    left_border: Char = "|"
    right_border: Char = "|"
    top_border: Char = "-"
    bottom_border: Char = "-"
