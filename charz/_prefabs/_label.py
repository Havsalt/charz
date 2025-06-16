from __future__ import annotations

from colex import ColorValue
from charz_core import Node, Vec2, Self

from ._sprite import Sprite
from .._annotations import Char


class Label(Sprite):
    r"""`Label` node to simplify displaying text.

    It extends `Sprite` and allows for easy text manipulation.
    The text is stored in the `texture` attribute, which is a list of strings.
    By using the `text` property, you can easily set and get the text.

    How tabs and newlines are handled can be customized with the following attributes:
    - `newline`: The character used to separate lines in the text.
        Default: `"\n"`
    - `tab_size`: The number of characters to use for each tab.
        Default: `4`
    - `tab_char`: The character to represent a tab.
        Default: `"\t"`
    - `tab_fill`: The character to use for filling in tabs.
        Default: `" "`

    Example:
    --------
    >>> import colex
    >>> from charz import Label, Scene
    ... # This will be placed in subclass of either `Engine`/`Scene`
    >>> class MenuPage(Scene):
    ...     def __init__(self) -> None:
    ...         self.label = Label(
    ...             text="Welcome to the game!\nPress [Enter] to start.",
    ...             color=colex.BLUE,
    ...             centered=True,
    ...         )
    """

    newline: Char = "\n"
    tab_size: int = 4
    tab_char: Char = "\t"
    tab_fill: Char = " "

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
        transparency: Char | None = None,
        color: ColorValue | None = None,
        text: str | None = None,
        newline: Char | None = None,
        tab_size: int | None = None,
        tab_char: Char | None = None,
        tab_fill: Char | None = None,
    ) -> None:
        Sprite.__init__(
            self,
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

    def with_newline(self, newline: Char, /) -> Self:
        """Chained method to set the newline character.

        Args:
            newline (Char): Newline character to use.

        Returns:
            Self: Same node instance.
        """
        self.newline = newline
        return self

    def with_tab_size(self, tab_size: int, /) -> Self:
        """Chained method to set the tab size.

        Args:
            tab_size (int): Tab size to use.

        Returns:
            Self: Same node instance.
        """
        self.tab_size = tab_size
        return self

    def with_tab_char(self, tab_char: Char, /) -> Self:
        """Chained method to set the tab character.

        Args:
            tab_char (Char): Tab character to use.

        Returns:
            Self: Same node instance.
        """
        self.tab_char = tab_char
        return self

    def with_tab_fill(self, tab_fill: Char, /) -> Self:
        """Chained method to set the tab fill character.

        Args:
            tab_fill (Char): Tab fill character to use.

        Returns:
            Self: Same node instance.
        """
        self.tab_fill = tab_fill
        return self

    def with_text(self, text: str, /) -> Self:
        """Chained method to set the text of the label.

        Args:
            text (str): Text to set as texture.

        Returns:
            Self: Same node instance.
        """
        self.text = text
        return self

    @property
    def text(self) -> str:
        """Get the text of the label.

        This replaces tabs with the node's fill character.

        Returns:
            str: The text of the label with tabs replaced by the fill character.
        """
        joined_lines = self.newline.join(self.texture)
        return joined_lines.replace(self.tab_fill * self.tab_size, self.tab_char)

    @text.setter
    def text(self, value: str) -> None:
        """Set the text of the label.

        This splits the text into lines and replaces tabs with the node's fill character.

        Args:
            value (str): The text to set as the label's texture.
        """
        tab_replaced = self.newline.replace(self.tab_char, self.tab_fill * self.tab_size)
        self.texture = value.split(tab_replaced)
