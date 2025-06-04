from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from charz_core import Vec2i, Self, group

from .. import text
from .._asset_loader import AssetLoader
from .._grouping import Group
from .._annotations import Char


# TODO: In future versions, add caching
def load_texture(
    texture_path: Path | str,
    /,
    *,
    flip_h: bool = False,
    flip_v: bool = False,
    fill: bool = True,
    fill_char: Char = " ",
) -> list[str]:
    """Load texture from file

    Args:
        texture_path (Path | str): Path to file with texture.
        flip_h (bool, optional): Flip horizontally. Defaults to False.
        flip_v (bool, optional): Flip vertically. Defaults to False.
        fill (bool, optional): Fill in to make shape rectangular. Defaults to True.
        fill_char (Char, optional): Filler string of length 1 to use. Defaults to " ".

    Returns:
        list[str]: Loaded texture

    Raises:
        ValueError: If `fill_char` is not of length `1`.
    """
    if len(fill_char) != 1:
        raise ValueError(
            f"Parameter 'fill_char' must of length 1, got {len(fill_char) = }"
        )
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
    """`TextureComponent` mixin class for node.

    Attributes:
        `texture`: `list[str]` - The texture data as a list of lines.
        `unique_texture`: `bool` - Whether the texture is unique per instance.
        `visible`: `bool` - Visibility state of the node.
        `centered`: `bool` - Whether the texture is centered.
        `z_index`: `int` - Z-order for rendering.
        `transparency`: `Char | None` - Character used to signal transparency.

    Methods:
        `hide`
        `show`
        `is_globally_visible`
        `get_texture_size`
    """

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
    transparency: Char | None = None

    def with_texture(self, texture_or_line: list[str] | str | Char, /) -> Self:
        """Chained method to set the texture of the node.

        If a string is provided, it is treated as a single line texture.

        Args:
            texture_or_line (list[str] | str | Char):
                Texture data as a list of lines, a single line string, or a character.

        Returns:
            Self: Same node instance.
        """
        if isinstance(texture_or_line, str):
            self.texture = [texture_or_line]
            return self
        self.texture = texture_or_line
        return self

    def with_unique_texture(self) -> Self:
        """Chained method to create a unique copy of texture as use that as `texture`.

        Returns:
            Self: Same node instance with a unique texture copy.
        """
        self.texture = deepcopy(self.texture)
        return self

    def with_visibility(self, state: bool = True, /) -> Self:
        """Chained method to set the visibility of the node.

        Args:
            state (bool, optional): Visibility state. Defaults to True.

        Returns:
            Self: Same node instance.
        """
        self.visible = state
        return self

    def with_centering(self, state: bool = True, /) -> Self:
        """Chained method to set whether the texture is centered.

        Args:
            state (bool, optional): Centering state. Defaults to True.

        Returns:
            Self: Same node instance.
        """
        self.centered = state
        return self

    def with_z_index(self, z_index: int, /) -> Self:
        """Chained method to set the z-index for rendering.

        Args:
            z_index (int): Z-index value.

        Returns:
            Self: Same node instance.
        """
        self.z_index = z_index
        return self

    def with_transparency(self, char: Char | None, /) -> Self:
        """Chained method to set the transparency character.

        Uses a string of length `1` as transparency character.
        If `None` is passed, no transparency is applied,
        which means strings with spaces will be rendered on top
        of other nodes with texture
        (as long as it has a greater z-index or the node is newer).

        Args:
            char (Char | None): Transparency character or `None`.

        Returns:
            Self: Same node instance.
        """
        self.transparency = char
        return self

    def hide(self) -> None:
        """Set the node to be hidden."""
        self.visible = False

    def show(self) -> None:
        """Set the node to be visible."""
        self.visible = True

    def is_globally_visible(self) -> bool:
        """Check whether the node and its ancestors are visible.

        Returns:
            bool: Global visibility.
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
        """Get the size of the texture.

        Computed in O(n*m), where n is the number of lines
        and m is the length of the longest line.

        Returns:
            Vec2i: Texture size.
        """
        if not self.texture:
            return Vec2i.ZERO
        return Vec2i(
            len(max(self.texture, key=len)),  # Length of longest line
            len(self.texture),  # Line count
        )
