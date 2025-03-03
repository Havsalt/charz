"""
Charz
=====

An object oriented terminal game engine

Includes
--------

- Annotations (from package `colex`)
  - `ColorValue`
- Math (from package `linflex`)
  - `lerp`
  - `sign`
  - `clamp`
  - `Vec2`
  - `Vec2i`
  - `Vec3`
- Modules
  - `text`
    - `fill`
    - `flip_h`
    - `flip_v`
    - `fill_lines`
    - `flip_lines_h`
    - `flip_lines_v`
    - `rotate`
  - `colex`    (dependency)
  - `keyboard` (optional dependency)
- Framework
  - `Engine`
  - `Clock`
  - `DeltaClock`
  - `Screen`
- Datastructures
  - `Animation`
  - `AnimationSet`
  - `Hitbox`
- Functions
  - `load_texture`
- Components
  - `Transform`
  - `Texture`
  - `Color`
  - `Animated`
  - `Collider`
- Nodes
  - `Camera`
  - `Node`
  - `Node2D`
  - `Sprite`
  - `Label`
  - `AnimatedSprite`
"""

__all__ = [
    "Engine",
    "Clock",
    "DeltaClock",
    "Screen",
    "Camera",
    "Node",
    "Node2D",
    "Transform",
    "lerp",
    "sign",
    "clamp",
    "Vec2",
    "Vec2i",
    "Vec3",
    "load_texture",
    "Texture",
    "Color",
    "ColorValue",
    "Label",
    "Sprite",
    "Animated",
    "AnimatedSprite",
    "Animation",
    "AnimationSet",
    "Collider",
    "Hitbox",
    "SimpleMovement",
    "text",
]

from typing import (
    TYPE_CHECKING as _TYPE_CHECKING,
    Literal as _Literal,
    Any as _Any,
)

# re-exports
from linflex import lerp, sign, clamp, Vec2, Vec2i, Vec3
from colex import ColorValue

# exports
from ._engine import Engine
from ._clock import Clock, DeltaClock
from ._screen import Screen
from ._camera import Camera
from ._node import Node
from ._animation import Animation, AnimationSet
from ._components._transform import Transform
from ._components._texture import load_texture, Texture
from ._components._color import Color
from ._components._animated import Animated
from ._components._collision import Collider, Hitbox
from ._prefabs._node2d import Node2D
from ._prefabs._label import Label
from ._prefabs._sprite import Sprite
from ._prefabs._animated_sprite import AnimatedSprite
from . import text


# provide correct completion help - even if the required feature is not active
if _TYPE_CHECKING:
    from ._components._simple_movement import SimpleMovement
else:
    # import `TYPE_CHECKING` here because the IDE can't handle the underscore
    from typing import TYPE_CHECKING  # this import won't be actually available at runtime

    if not TYPE_CHECKING:
        SimpleMovement = NotImplemented
    del TYPE_CHECKING  # delete it to error on import

# lazy exports
_lazy_objects: tuple[_Literal["SimpleMovement"]] = ("SimpleMovement",)
_loaded_objects: dict[str, object] = {
    name: obj
    for name, obj in globals().items()
    if name in __all__ and name not in _lazy_objects
}


# lazy load to properly load optional dependencies along the standard exports
def __getattr__(name: str) -> _Any:
    global _loaded_objects
    if name in _loaded_objects:
        return _loaded_objects[name]
    elif name in _lazy_objects:
        # NOTE: manually add each branch
        if name == "SimpleMovement":
            from ._components._simple_movement import SimpleMovement

            _loaded_objects[name] = SimpleMovement
            return _loaded_objects[name]
        else:
            raise NotImplementedError(f"branch not implemented for '{name}'")
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
