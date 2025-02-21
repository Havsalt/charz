from __future__ import annotations

from pathlib import Path
from copy import deepcopy
from typing import Any, ClassVar

from linflex import Vec2i
from typing_extensions import Self

from .. import text
from .._annotations import TextureNode


def load_texture(
    file_path: Path | str,
    /,
    *,
    flip_h: bool = False,
    flip_v: bool = False,
    fill: bool = True,
    fill_char: str = " ",
) -> list[str]:
    """Loads texture from file

    Args:
        file_path (Path | str): path to file.
        flip_h (bool, optional): flip horizontally. Defaults to False.
        flip_v (bool, optional): flip vertically. Defaults to False.
        fill (bool, optional): fill in to make shape rectangular. Defaults to True.
        fill_char (str, optional): string of length 1 to fill with. Defaults to " ".

    Returns:
        list[str]: loaded texture
    """
    file = Path.cwd().joinpath(str(file_path))
    content = file.read_text(encoding="utf-8")
    texture = content.splitlines()
    if fill:  # NOTE: this fill logic has to be before flipping
        texture = text.fill_lines(texture, fill_char=fill_char)
    if flip_h:
        texture = text.flip_lines_h(texture)
    if flip_v:
        texture = text.flip_lines_v(texture)
    return texture


class Texture:  # Component (mixin class)
    texture_instances: ClassVar[dict[int, TextureNode]] = {}

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        Texture.texture_instances[instance.uid] = instance  # type: ignore
        if (class_texture := getattr(instance, "texture", None)) is not None:
            instance.texture = deepcopy(class_texture)
        else:
            instance.texture = []
        return instance

    texture: list[str]
    visible: bool = True
    centered: bool = False
    z_index: int = 0
    transparency: str | None = None

    def with_texture(self, texture_or_line: list[str] | str, /) -> Self:
        if isinstance(texture_or_line, str):
            self.texture = [texture_or_line]
            return self
        self.texture = texture_or_line
        return self

    def as_visible(self, state: bool = True, /) -> Self:
        self.visible = state
        return self

    def as_centered(self, state: bool = True, /) -> Self:
        self.centered = state
        return self

    def with_z_index(self, z_index: int, /) -> Self:
        self.z_index = z_index
        return self

    def with_transparency(self, char: str | None, /) -> Self:
        self.transparancy = char
        return self

    def hide(self) -> None:
        self.visible = False

    def show(self) -> None:
        self.visible = True

    def is_globally_visible(self) -> bool:  # global visibility
        """Checks whether the node and its ancestors are visible

        Returns:
            bool: global visibility
        """
        if not self.visible:
            return False
        parent = self.parent  # type: ignore
        while parent is not None:
            if not isinstance(parent, Texture):
                return True
            if not parent.visible:
                return False
            parent = parent.parent  # type: ignore
        return True

    @property
    def texture_size(self) -> Vec2i:
        """Get the size of the texture

        Computed in O(n*m), where n is the number of lines and m is the length of the longest line

        Returns:
            Vec2i: texture size
        """  # noqa: E501
        if not self.texture:
            return Vec2i.ZERO
        return Vec2i(
            len(max(self.texture, key=len)),  # size of longest line
            len(self.texture),  # line count
        )

    def _free(self) -> None:
        del Texture.texture_instances[self.uid]  # type: ignore
        super()._free()  # type: ignore
