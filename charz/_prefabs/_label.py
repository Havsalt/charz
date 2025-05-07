from __future__ import annotations

from colex import ColorValue
from charz_core import Node, Vec2, Self

from ._sprite import Sprite


class Label(Sprite):
    newline: str = "\n"
    tab_size: int = 4
    tab_char: str = "\t"
    tab_fill: str = " "

    def __init__(
        self,
        parent: Node | None = None,
        *,
        position: Vec2 | None = None,
        rotation: float | None = None,
        top_level: bool | None = None,
        texture: list[str] | None = None,
        visible: bool | None = None,
        centered: bool | None = None,
        z_index: int | None = None,
        transparency: str | None = None,
        color: ColorValue | None = None,
        text: str | None = None,
        newline: str | None = None,
        tab_size: int | None = None,
        tab_char: str | None = None,
        tab_fill: str | None = None,
    ) -> None:
        super().__init__(
            parent=parent,
            position=position,
            rotation=rotation,
            top_level=top_level,
            texture=texture,
            visible=visible,
            centered=centered,
            z_index=z_index,
            transparency=transparency,
            color=color,
        )
        if text is not None:
            self.text = text
        if newline is not None:
            self.newline = newline
        if tab_size is not None:
            self.tab_size = tab_size
        if tab_char is not None:
            self.tab_char = tab_char
        if tab_fill is not None:
            self.tab_fill = tab_fill

    def with_newline(self, newline: str, /) -> Self:
        self.newline = newline
        return self

    def with_tab_size(self, tab_size: int, /) -> Self:
        self.tab_size = tab_size
        return self

    def with_tab_char(self, tab_char: str, /) -> Self:
        self.tab_char = tab_char
        return self

    def with_tab_fill(self, tab_fill: str, /) -> Self:
        self.tab_fill = tab_fill
        return self

    def with_text(self, text: str, /) -> Self:
        self.text = text
        return self

    @property
    def text(self) -> str:
        joined_lines = self.newline.join(self.texture)
        return joined_lines.replace(self.tab_fill * self.tab_size, self.tab_char)

    @text.setter
    def text(self, value: str) -> None:
        tab_replaced = self.newline.replace(self.tab_char, self.tab_fill * self.tab_size)
        self.texture = value.split(tab_replaced)
