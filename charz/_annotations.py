"""
Custom Annotations for `charz`
===================================

This file contains private annotations used across this package.

Whenever there is a "?" comment,
it means a type may or may not implement that field or mixin class.
"""

from __future__ import annotations as _annotations

from typing import (
    TypeVar as _TypeVar,
    TypeAlias as _TypeAlias,
    Protocol as _Protocol,
    overload as _overload,
    runtime_checkable as _runtime_checkable,
    TYPE_CHECKING as _TYPE_CHECKING,
)

from charz_core import (
    Vec2 as _Vec2,
    Vec2i as _Vec2i,
)
from colex import ColorValue as _ColorValue
from typing_extensions import LiteralString as _LiteralString

if _TYPE_CHECKING:
    from charz_core import Self as _Self
    from ._clock import Clock as _Clock
    from ._screen import Screen as _Screen
    from ._components._collision import Hitbox as _Hitbox
    from ._animation import (
        Animation as _Animation,
        AnimationSet as _AnimationSet,
    )

T = _TypeVar("T")
Number = _TypeVar("Number", float, int)
_T_contra = _TypeVar("_T_contra", contravariant=True)
Char: _TypeAlias = str  # Signifying `str` of length `1`


@_runtime_checkable
class FileLike(_Protocol[_T_contra]):
    def write(self, stream: _T_contra, /) -> object: ...
    def flush(self, /) -> None: ...
    def fileno(self, /) -> int: ...


class Engine(_Protocol):
    fps: float
    clock: _Clock
    screen: _Screen
    _is_running: bool

    @property
    def is_running(self) -> bool: ...
    @is_running.setter
    def is_running(self, run_state: bool) -> None: ...


class Node(_Protocol):
    uid: int

    def __init__(self) -> None: ...
    def with_parent(self, parent: Node | None, /) -> _Self: ...
    def update(self) -> None: ...
    def queue_free(self) -> None: ...
    def _free(self) -> None: ...


class TransformComponent(_Protocol):
    position: _Vec2
    rotation: float
    top_level: bool

    @_overload
    def with_position(
        self,
        position: _Vec2,
        /,
    ) -> _Self: ...
    @_overload
    def with_position(
        self,
        *,
        x: float,
        y: float,
    ) -> _Self: ...
    @_overload
    def with_global_position(
        self,
        global_position: _Vec2,
        /,
    ) -> _Self: ...
    @_overload
    def with_global_position(
        self,
        *,
        x: float,
        y: float,
    ) -> _Self: ...
    def with_rotation(self, rotation: float, /) -> _Self: ...
    def with_global_rotation(self, global_rotation: float, /) -> _Self: ...
    def with_top_level(self, state: bool = True, /) -> _Self: ...
    @property
    def global_position(self) -> _Vec2: ...
    @global_position.setter
    def global_position(self, position: _Vec2) -> None: ...
    @property
    def global_rotation(self) -> float: ...
    @global_rotation.setter
    def global_rotation(self, rotation: float) -> None: ...


class TransformNode(
    TransformComponent,
    Node,
    _Protocol,
): ...


class TextureComponent(_Protocol):
    texture: list[str]
    unique_texture: bool
    visible: bool
    centered: bool
    z_index: int
    transparency: Char | None

    def with_texture(self, texture_or_line: list[str] | str | Char, /) -> _Self: ...
    def with_unique_texture(self) -> _Self: ...
    def with_visibility(self, state: bool = True, /) -> _Self: ...
    def with_centering(self, state: bool = True, /) -> _Self: ...
    def with_z_index(self, z_index: int, /) -> _Self: ...
    def with_transparency(self, char: Char | None, /) -> _Self: ...
    def hide(self) -> None: ...
    def show(self) -> None: ...
    def is_globally_visible(self) -> bool: ...
    def get_texture_size(self) -> _Vec2i: ...


class TextureNode(
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol,
): ...


class ColorComponent(_Protocol):
    color: _ColorValue | None

    def with_color(
        self,
        color: _ColorValue | None,
        /,
    ) -> _Self: ...


class ColorNode(
    ColorComponent,
    TextureComponent,
    TransformNode,
    Node,
    _Protocol,
): ...


class Renderable(
    # `ColorComponent`?
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol,
): ...


class AnimatedComponent(_Protocol):
    animations: _AnimationSet
    current_animation: _Animation | None
    repeat: bool
    is_playing: bool

    def with_animations(self, **animations: _Animation) -> _Self: ...
    def with_animation(
        self,
        animation_name: str,
        animation: _Animation,
        /,
    ) -> _Self: ...
    def with_repeat(self, state: bool = True, /) -> _Self: ...
    def add_animation(
        self,
        animation_name: str,
        animation: _Animation,
    ) -> None: ...
    def play(self, animation_name: str, /) -> None: ...
    def play_backwards(self, animation_name: str, /) -> None: ...
    def progress_animation(self) -> None: ...


class AnimatedNode(
    # `ColorComponent`?
    AnimatedComponent,
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol,
): ...


class ColliderComponent(_Protocol):
    hitbox: _Hitbox

    def with_hitbox(self, hitbox: _Hitbox, /) -> _Self: ...
    def get_colliders(self) -> list[ColliderNode]: ...
    def is_colliding_with(self, colldier_node: ColliderNode, /) -> bool: ...
    def is_colliding(self) -> bool: ...


class ColliderNode(
    # `ColorComponent`?
    # `TextureComponent`?
    ColliderComponent,
    TransformComponent,
    Node,
    _Protocol,
): ...
