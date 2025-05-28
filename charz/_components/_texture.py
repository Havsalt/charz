from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from charz_core import Vec2i, Self, group

from .. import text
from .._asset_loader import AssetLoader
from .._grouping import Group


# TODO: In future versions, add caching
def load_texture(
    texture_path: Path | str,
    /,
    *,
    flip_h: bool = False,
    flip_v: bool = False,
    fill: bool = True,
    fill_char: str = " ",
) -> list[str]:
    """Load texture from file

    Args:
        texture_path (Path | str): Path to file with texture.
        flip_h (bool, optional): Flip horizontally. Defaults to False.
        flip_v (bool, optional): Flip vertically. Defaults to False.
        fill (bool, optional): Fill in to make shape rectangular. Defaults to True.
        fill_char (str, optional): Filler string of length 1 to use. Defaults to " ".

    Returns:
        list[str]: Foaded texture
    """
    # fmt: off
    file = (
        Path.cwd()
        .joinpath(AssetLoader.texture_root)
        .joinpath(texture_path)
    )
    # fmt: on
    content = file.read_text(encoding="utf-8")
    texture = content.splitlines()
    if fill:  # NOTE: This fill logic has to be before flipping
        texture = text.fill_lines(texture, fill_char=fill_char)
    if flip_h:
        texture = text.flip_lines_h(texture)
    if flip_v:
        texture = text.flip_lines_v(texture)
    return texture


@group(Group.TEXTURE)
class TextureComponent:  # Component (mixin class)
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        if (class_texture := getattr(instance, "texture", None)) is not None:
            if instance.unique_texture:
                instance.texture = deepcopy(class_texture)
            else:
                instance.texture = class_texture
        else:
            instance.texture = []
        return instance

    texture: list[str]
    unique_texture: bool = True
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

    def with_visibility(self, state: bool = True, /) -> Self:
        self.visible = state
        return self

    def with_centering(self, state: bool = True, /) -> Self:
        self.centered = state
        return self

    def with_z_index(self, z_index: int, /) -> Self:
        self.z_index = z_index
        return self

    def with_transparency(self, char: str | None, /) -> Self:
        self.transparency = char
        return self

    def hide(self) -> None:
        self.visible = False

    def show(self) -> None:
        self.visible = True

    def is_globally_visible(self) -> bool:
        """Check whether the node and its ancestors are visible

        Returns:
            bool: Blobal visibility
        """
        if not self.visible:
            return False
        parent = self.parent  # type: ignore
        while parent is not None:
            if not isinstance(parent, TextureComponent):
                return True
            if not parent.visible:
                return False
            parent = parent.parent  # type: ignore
        return True

    def get_texture_size(self) -> Vec2i:
        """Get the size of the texture

        Computed in O(n*m), where n is the number of lines
        and m is the length of the longest line

        Returns:
            Vec2i: Texture size
        """
        if not self.texture:
            return Vec2i.ZERO
        return Vec2i(
            len(max(self.texture, key=len)),  # Length of longest line
            len(self.texture),  # Line count
        )
