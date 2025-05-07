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
  - `DeltaClock`
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
  - `Transform`
  - `Texture`
  - `Color`
  - `Animated`
  - `Collider`
- Nodes
  - `Node`
  - `Node2D`
  - `Camera`
  - `Sprite`
  - `Label`
  - `AnimatedSprite`
"""

__all__ = [
    # Annotations
    "ColorValue",
    "Self",
    # Math
    "lerp",
    "sign",
    "clamp",
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
    "Transform",
    "Texture",
    "Color",
    "Animated",
    "Collider",
    # Nodes
    "Node",
    "Node2D",
    "Camera",
    "Sprite",
    "Label",
    "AnimatedSprite",
]

from typing import TYPE_CHECKING as _TYPE_CHECKING

# re-exports
from colex import ColorValue

# re-exports from `charz-core`
from charz_core import (
    Self,
    lerp,
    sign,
    clamp,
    Vec2,
    Vec2i,
    Vec3,
    Scene,
    group,
    Transform,
    Node,
    Node2D,
    Camera,
)

# exports
from ._engine import Engine
from ._clock import Clock
from ._screen import Screen
from ._time import Time
from ._asset_loader import AssetLoader
from ._grouping import Group
from ._animation import Animation, AnimationSet
from ._components._texture import load_texture, Texture
from ._components._color import Color
from ._components._animated import Animated
from ._components._collision import Collider, Hitbox
from ._prefabs._sprite import Sprite
from ._prefabs._label import Label
from ._prefabs._animated_sprite import AnimatedSprite
from . import text


# provide correct completion help - even if the required feature is not active
if _TYPE_CHECKING:
    from ._components._simple_movement import SimpleMovement

# lazy exports
# NOTE: add to `_lazy_objects` when adding new export
_lazy_objects = ("SimpleMovement",)
_loaded_objects: dict[str, object] = {
    name: obj
    for name, obj in globals().items()
    if name in __all__ and name not in _lazy_objects
}


# lazy load to properly load optional dependencies along the standard exports
# TODO: check if there is a step here that can be skipped
def __getattr__(name: str) -> object:
    if name in _loaded_objects:
        return _loaded_objects[name]
    elif name in _lazy_objects:
        # NOTE: manually add each branch
        match name:
            case "SimpleMovement":
                from ._components._simple_movement import SimpleMovement

                _loaded_objects[name] = SimpleMovement
                return _loaded_objects[name]
            case _:
                raise NotImplementedError(f"branch not implemented for '{name}'")
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
