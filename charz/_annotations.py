from __future__ import annotations as _annotations

from typing import (
    TypeVar as _TypeVar,
    Protocol as _Protocol,
    Callable as _Callable,
    Any as _Any,
    TYPE_CHECKING as _TYPE_CHECKING
)

from linflex import Vec2 as _Vec2
from colex import ColorValue as _ColorValue

if _TYPE_CHECKING:
    from ._clock import DeltaClock as _DeltaClock
    from ._screen import Screen as _Screen
    from ._animation import Animation as _Animation

EngineType = _TypeVar("EngineType", bound="Engine", covariant=True)
NodeType = _TypeVar("NodeType", bound="Node", covariant=True)
_Self = _TypeVar("_Self")
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
    def __init__(self) -> None: ...
    def setup(self) -> None: ...
    def update(self, delta: float) -> None: ...
    def queue_free(self) -> None: ...
    def free(self) -> None: ...


class TransformComponent(_Protocol):
    position: _Vec2
    @property
    def global_position(self) -> _Vec2: ...
    @global_position.setter
    def global_position(self, position: _Vec2) -> None: ...


class TransformNode(
    TransformComponent,
    Node,
    _Protocol
): ...


class TextureComponent(_Protocol):
    texture: list[str]


class TextureNode(
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol
): ...


class ColorComponent(_Protocol):
    color: _ColorValue | None
    def with_color(
        self: _Self,
        color: _ColorValue,
        /
    ) -> _Self: ...


class ColorNode(
    ColorComponent,
    TextureComponent,
    TransformNode,
    Node,
    _Protocol
): ...


class Renderable(
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol
): ...
    # color?: _ColorValue


class Animated(_Protocol):
    animations: dict[str, _Any]
    current_animation: _Animation | None = None
    _frame_index: int = 0
    def with_animations(self: _Self, animations: dict[str, _Any], /) -> _Self: ...
    def play(self, animation_name: str) -> None: ...
    def _wrapped_update_animated(self, delta: float) -> None: ...


class AnimatedNode(
    Animated,
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol
    # Color?
): ...
