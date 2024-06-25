from __future__ import annotations as _annotations

from types import UnionType as _UnionType
from typing import (
    TypeVar as _TypeVar,
    TypeAlias as _TypeAlias,
    Protocol as _Protocol,
    TYPE_CHECKING as _TYPE_CHECKING
)

from linflex import Vec2 as _Vec2
from colex import ColorValue as _ColorValue

if _TYPE_CHECKING:
    from ._clock import DeltaClock as _DeltaClock
    from ._screen import Screen as _Screen

EngineType = _TypeVar("EngineType", bound="Engine", covariant=True)
NodeType = _TypeVar("NodeType", bound="Node", covariant=True)
_T_contra = _TypeVar("_T_contra", contravariant=True)


class FileLike(_Protocol[_T_contra]):
    def write(self, stream: _T_contra, /) -> object: ...
    def flush(self, /) -> None: ...


class Engine(_Protocol):
    fps: float
    clock: _DeltaClock
    screen: _Screen
    is_running: bool


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