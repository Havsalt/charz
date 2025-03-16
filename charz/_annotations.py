"""
Custom Annotations for Charz
============================

This file contains private annotations used across this package.

Whenever there is a "?" comment,
it means a type may or may not implement that field or mixin class.
"""

from __future__ import annotations as _annotations


from typing import (
    TypeVar as _TypeVar,
    Protocol as _Protocol,
    ClassVar as _ClassVar,
    runtime_checkable as _runtime_checkable,
    TYPE_CHECKING as _TYPE_CHECKING,
)

from linflex import (
    Vec2 as _Vec2,
    Vec2i as _Vec2i,
)
from colex import ColorValue as _ColorValue
from typing_extensions import Self as _Self

if _TYPE_CHECKING:
    from ._clock import DeltaClock as _DeltaClock
    from ._screen import Screen as _Screen
    from ._animation import (
        Animation as _Animation,
        AnimationSet as _AnimationMapping,
    )
    from ._components._collision import Hitbox as _Hitbox

T = _TypeVar("T")
_T_contra = _TypeVar("_T_contra", contravariant=True)


@_runtime_checkable
class FileLike(_Protocol[_T_contra]):
    def write(self, stream: _T_contra, /) -> object: ...
    def flush(self, /) -> None: ...
    def fileno(self, /) -> int: ...


@_runtime_checkable
class Engine(_Protocol):
    fps: float
    clock: _DeltaClock
    screen: _Screen
    is_running: bool


@_runtime_checkable
class Node(_Protocol):
    node_instances: _ClassVar[dict[int, Node]]
    uid: int

    def __init__(self) -> None: ...
    def with_parent(self, parent: Node | None, /) -> _Self: ...
    def with_process_priority(self, process_priority: int, /) -> _Self: ...
    def update(self, delta: float) -> None: ...
    def queue_free(self) -> None: ...
    def _free(self) -> None: ...


class TransformComponent(_Protocol):
    position: _Vec2
    rotation: float
    top_level: bool

    def with_position(
        self,
        position: _Vec2 | None = None,
        /,
        x: float | None = None,
        y: float | None = None,
    ) -> _Self: ...
    def with_global_position(
        self,
        global_position: _Vec2 | None = None,
        /,
        x: float | None = None,
        y: float | None = None,
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


@_runtime_checkable
class TransformNode(
    TransformComponent,
    Node,
    _Protocol,
): ...


class TextureComponent(_Protocol):
    texture_instances: _ClassVar[dict[int, TextureNode]]
    texture: list[str]
    visible: bool
    centered: bool
    z_index: int
    transparency: str | None

    def with_texture(self, texture_or_line: list[str] | str, /) -> _Self: ...
    def with_visibility(self, state: bool = True, /) -> _Self: ...
    def with_centering(self, state: bool = True, /) -> _Self: ...
    def with_z_index(self, z_index: int, /) -> _Self: ...
    def with_transparency(self, char: str | None, /) -> _Self: ...
    def hide(self) -> None: ...
    def show(self) -> None: ...
    def is_globally_visible(self) -> bool: ...
    @property
    def texture_size(self) -> _Vec2i: ...


@_runtime_checkable
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


@_runtime_checkable
class ColorNode(
    ColorComponent,
    TextureComponent,
    TransformNode,
    Node,
    _Protocol,
): ...


@_runtime_checkable
class Renderable(
    # `ColorComponent`?
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol,
): ...


class AnimatedComponent(_Protocol):
    animations: _AnimationMapping
    current_animation: _Animation | None = None

    def with_animations(self, **animations: _Animation) -> _Self: ...
    def with_animation(
        self,
        animation_name: str,
        animation: _Animation,
        /,
    ) -> _Self: ...
    def add_animation(
        self,
        animation_name: str,
        animation: _Animation,
    ) -> None: ...
    def play(self, animation_name: str, /) -> None: ...
    def play_backwards(self, animation_name: str, /) -> None: ...
    def _wrapped_update_animated(self, _delta: float) -> None: ...


@_runtime_checkable
class AnimatedNode(
    # `ColorComponent`?
    AnimatedComponent,
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol,
): ...


class ColliderComponent(_Protocol):
    collider_instances: _ClassVar[dict[int, ColliderNode]]
    hitbox: _Hitbox
    disabled: bool

    def with_hitbox(self, hitbox: _Hitbox, /) -> _Self: ...
    def with_disabled(self, state: bool = True, /) -> _Self: ...
    def get_colliders(self) -> list[ColliderNode]: ...
    def is_colliding_with(self, colldier_node: ColliderNode, /) -> bool: ...
    def is_colliding(self) -> bool: ...


@_runtime_checkable
class ColliderNode(
    # `ColorComponent`?
    # `TextureComponent`?
    ColliderComponent,
    TransformComponent,
    Node,
    _Protocol,
): ...
