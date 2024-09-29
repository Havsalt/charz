from __future__ import annotations as _annotations

from pathlib import Path as _Path
from copy import deepcopy as _deepcopy
from typing import (
    Any as _Any,
    ClassVar as _ClassVar,
)

from linflex import Vec2i as _Vec2i
from typing_extensions import Self as _Self

from .._annotations import (
    NodeType as _NodeType,
    TextureNode as _TextureNode,
)


def load_texture(file_path: _Path | str, /) -> list[str]:
    return _Path.cwd().joinpath(str(file_path)).read_text(encoding="utf-8").splitlines()


class Texture:  # Component (mixin class)
    texture_instances: _ClassVar[dict[int, _TextureNode]] = {}

    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs)  # type: _TextureNode  # type: ignore[reportAssignmentType]
        Texture.texture_instances[instance.uid] = instance
        if (class_texture := getattr(instance, "texture", None)) is not None:
            instance.texture = _deepcopy(class_texture)
        else:
            instance.texture = []
        return instance  # type: ignore

    texture: list[str]
    visible: bool = True
    centered: bool = False
    transparency: str | None = None

    def with_texture(self, texture_or_line: list[str] | str, /) -> _Self:
        if isinstance(texture_or_line, str):
            self.texture = [texture_or_line]
            return self
        self.texture = texture_or_line
        return self

    def as_visible(self, state: bool = True, /) -> _Self:
        self.visible = state
        return self

    def as_centered(self, state: bool = True, /) -> _Self:
        self.centered = state
        return self

    def with_transparency(self, char: str | None, /) -> _Self:
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

    def get_texture_size(self) -> _Vec2i:
        if not self.texture:
            return _Vec2i.ZERO
        return _Vec2i(
            len(max(self.texture, key=len)),  # size of longest line
            len(self.texture),  # line count
        )

    def free(self: _TextureNode) -> None:
        del Texture.texture_instances[self.uid]
        super().free()
