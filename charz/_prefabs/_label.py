from __future__ import annotations as _annotations

from .._node import Node as _Node
from .._transform import Transform as _Transform
from .._texture import Texture as _Texture
from .._color import Color as _Color


class Label(_Color, _Texture, _Transform, _Node):
    newline: str = "\n"
    tab_size: int = 4
    tab_char: str = "\t"
    tab_fill: str = " "

    def with_newline(self, newline: str, /):
        self.newline = newline
        return self

    def with_tab_size(self, tab_size: int, /):
        self.tab_size = tab_size
        return self

    def with_tab_char(self, tab_char: str, /):
        self.tab_char = tab_char
        return self

    def with_tab_fill(self, tab_fill: str, /):
        self.tab_fill = tab_fill
        return self

    def with_text(self, text: str, /):
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
