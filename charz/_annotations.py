from __future__ import annotations as _annotations

from typing import (
    TypeVar as _TypeVar,
    Protocol as _Protocol
)

from linflex import Vec2 as _Vec2
from colex import ColorValue as _ColorValue

NodeType = _TypeVar("NodeType")
_T_contra = _TypeVar("_T_contra", contravariant=True)


class FileLike(_Protocol[_T_contra]):
    def write(self, stream: _T_contra, /) -> object: ...
    def flush(self, /) -> None: ...


class Node(_Protocol):
    uid: int


class TransformComponent(_Protocol):
    position: _Vec2
    @property
    def global_position(self) -> _Vec2: ...
    @global_position.setter
    def global_position(self, position: _Vec2) -> None: ...


class TransformNode(TransformComponent, Node, _Protocol): ...


class TextureComponent(_Protocol):
    texture: list[str]


class TextureNode(TextureComponent, TransformComponent, Node, _Protocol): ...


class ColorComponent(_Protocol):
    color: _ColorValue | None


class ColorNode(ColorComponent, TextureComponent, TransformNode, Node, _Protocol): ...


class Renderable(TextureComponent, TransformComponent, Node, _Protocol): ...
    # color?: _ColorValue