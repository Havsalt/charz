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

from typing import TYPE_CHECKING as _TYPE_CHECKING

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
# NOTE: Add to `_lazy_objects` when adding new export
_lazy_objects = ("SimpleMovementComponent",)
_loaded_objects: dict[str, object] = {
    name: lazy_object
    for name, lazy_object in globals().items()
    if name in __all__ and name not in _lazy_objects
}


# Lazy load to properly load optional dependencies along the standard exports
def __getattr__(name: str) -> object:
    if name in _loaded_objects:
        return _loaded_objects[name]
    elif name in _lazy_objects:
        # NOTE: Manually add each case branch
        match name:
            case "SimpleMovementComponent":
                from ._components._simple_movement import SimpleMovementComponent

                _loaded_objects[name] = SimpleMovementComponent
                return _loaded_objects[name]
            case _:
                raise NotImplementedError(f"Case branch not implemented for '{name}'")
    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")
