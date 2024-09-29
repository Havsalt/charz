"""
Charz
-----

An object oriented terminal game engine

Includes:
- `Engine` (derive new App class from this)
- `Clock` (calculates delta time)
- `DeltaClock` (controls framerate)
- `Screen` (renders nodes to console)
- `Camera` (handles viewport)
- `CameraMode` (enum)
- `Node` (base node)
- `Node2D` (prefabricated, node in world)
- `Transform` (component)
- `lerp` (function from `linflex` package)
- `sign` (function from `linflex` package)
- `clamp` (function from `linflex` package)
- `Vec2` (datastructure from `linflex` package)
- `Vec2i` (datastructure from `linflex` package)
- `Vec3` (datastructure from `linflex` package)
- `load_texture` (function)
- `Texture` (component)
- `Color` (component)
- `ColorValue` (annotation from `colex` package)
- `Label` (prefabricated)
- `Sprite` (prefabricated)
- `AnimatedSprite` (prefabricated)
- `Animation` (datastructure)
- `Collider` (component)
- `Hitbox` (datastructure)
- `text` (module for flipping strings)
"""

from __future__ import annotations as _annotations

__version__ = "0.0.22"
__all__ = [
    "Engine",
    "Clock",
    "DeltaClock",
    "Screen",
    "Camera",
    "CameraMode",
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
    "AnimatedSprite",
    "Animation",
    "Collider",
    "Hitbox",
    "text",
]

from linflex import lerp, sign, clamp, Vec2, Vec2i, Vec3
from colex import ColorValue

from ._engine import Engine
from ._clock import Clock, DeltaClock
from ._screen import Screen
from ._camera import Camera, CameraMode
from ._node import Node
from ._components._transform import Transform
from ._components._texture import load_texture, Texture
from ._components._color import Color
from ._components._animation import Animation
from ._components._collision import Collider, Hitbox
from ._prefabs._node2d import Node2D
from ._prefabs._label import Label
from ._prefabs._sprite import Sprite
from ._prefabs._animated_sprite import AnimatedSprite
from . import text
