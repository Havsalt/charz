"""
Charz
=====

An object oriented terminal game engine

Includes
--------

- Annotations
  - `ColorValue`  (from package `colex`)
  - `Self`        (from standard `typing` or from package `typing-extensions`)
- Math (from package `linflex`)
  - `lerp`
  - `sign`
  - `clamp`
  - `move_toward`
  - `Vec2`
  - `Vec2i`
  - `Vec3`
- Submodules
  - `text`
    - `fill`
    - `flip_h`
    - `flip_v`
    - `fill_lines`
    - `flip_lines_h`
    - `flip_lines_v`
    - `rotate`
- Framework
  - `Engine`
  - `Clock`
  - `Screen`
  - `Scene`
- Datastructures
  - `Animation`
  - `AnimationSet`
  - `Hitbox`
- Functions
  - `load_texture`
- Decorators
  - `group`
- Enums
  - `Group`
- Components
  - `TransformComponent`
  - `TextureComponent`
  - `ColorComponent`
  - `AnimatedComponent`
  - `ColliderComponent`
- Nodes
  - `Node`
  - `Node2D`
  - `Camera`
  - `Sprite`
  - `Label`
  - `AnimatedSprite`
- Feature dependent
  - `SimpleMovementComponent` (when using feature `keyboard`/`all`)
"""

from __future__ import annotations as _annotations

__all__ = [
    # Annotations
    "ColorValue",
    "Self",
    # Math
    "lerp",
    "sign",
    "clamp",
    "move_toward",
    "Vec2",
    "Vec2i",
    "Vec3",
    # Submodules
    "text",
    # Framework
    "Engine",
    "Clock",
    "Screen",
    "Scene",
    "AssetLoader",
    # Datastructures
    "Animation",
    "AnimationSet",
    "Hitbox",
    # Functions
    "load_texture",
    # Decorators
    "group",
    # Enums
    "Group",
    # Singletons
    "Time",
    "AssetLoader",
    # Components
    "TransformComponent",
    "TextureComponent",
    "ColorComponent",
    "AnimatedComponent",
    "ColliderComponent",
    # Nodes
    "Node",
    "Node2D",
    "Camera",
    "Sprite",
    "Label",
    "AnimatedSprite",
]

from typing import (
    TYPE_CHECKING as _TYPE_CHECKING,
    TypeAlias as _TypeAlias,
    Literal as _Literal,
    Any as _Any,
    overload as _overload,
    get_args as _get_args,
)

from typing_extensions import assert_never as _assert_never

# Re-exports from `colex`
from colex import ColorValue

# Re-exports from `charz-core`
from charz_core import (
    Self,
    lerp,
    sign,
    clamp,
    move_toward,
    Vec2,
    Vec2i,
    Vec3,
    group,
    TransformComponent,
    Node,
    Node2D,
    Scene,
    Camera,
)

# Exports
from ._engine import Engine
from ._clock import Clock
from ._screen import Screen
from ._time import Time
from ._asset_loader import AssetLoader
from ._grouping import Group
from ._animation import Animation, AnimationSet
from ._components._texture import load_texture, TextureComponent
from ._components._color import ColorComponent
from ._components._animated import AnimatedComponent
from ._components._collision import ColliderComponent, Hitbox
from ._prefabs._sprite import Sprite
from ._prefabs._label import Label
from ._prefabs._animated_sprite import AnimatedSprite
from . import text

# Import to add scene frame tasks
from . import _scene_tasks


# Provide correct completion help - Even if the required feature is not active
if _TYPE_CHECKING:
    from ._components._simple_movement import SimpleMovementComponent

# Lazy exports
# NOTE: Literals and `__getattr__` case branches has to be implemented manually
_LazyNames: _TypeAlias = _Literal["SimpleMovementComponent"]
# NOTE: Add string to `Literal` when a new branch is added
# _LazyNames: _TypeAlias = _Literal["SimpleMovementComponent", "ExampleLazyObject"]
_lazy_object_names = _get_args(_LazyNames)
_lazy_loaded_objects: dict[str, _Any] = {}


# Lazy load to properly load optional dependencies along the standard exports
# NOTE: Using "type: ignore" since it takes multiple branches to work properly
@_overload
def __getattr__(name: _Literal["SimpleMovementComponent"]): ...  # type: ignore  # noqa: ANN202
# @_overload
# def __getattr__(name: _Literal["ExampleLazyObject"]): ...
def __getattr__(name: _LazyNames):
    if name in _lazy_loaded_objects:
        return _lazy_loaded_objects[name]
    elif name in _lazy_object_names:
        # NOTE: Manually add each case branch
        match name:
            case "SimpleMovementComponent":
                from ._components._simple_movement import SimpleMovementComponent  # noqa: PLC0415

                _lazy_loaded_objects[name] = SimpleMovementComponent
                return _lazy_loaded_objects[name]
            case _:
                _assert_never(name)
    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")
