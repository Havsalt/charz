"""
Charz
--------

An object oriented terminal game engine

Includes:
- `Engine`
- `Clock`
- `DeltaClock`
- `Screen`
- `Camera`
- `CameraMode` (enum)
- `Node` (base node)
- `Node2D`
- `Transform` (component)
- `Vec2` (datastructure from `linflex` package)
- `Texture` (component)
- `Color` (component)
- `ColorValue` (annotation from `colex` package)
- `Label` (prefabricated)
- `Sprite` (prefabricated)
- `AnimatedSprite` (prefabricated)
- `Animation` (datastructure)
- `text` (module for flipping strings)
"""

from __future__ import annotations as _annotations

__version__ = "0.0.10"
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
    "Vec2",
    "load_texture",
    "Texture",
    "Color",
    "ColorValue",
    "Label",
    "Sprite",
    "AnimatedSprite",
    "Animation",
    "text"
]

from linflex import Vec2
from colex import ColorValue

from ._engine import Engine
from ._clock import Clock, DeltaClock
from ._screen import Screen
from ._camera import Camera, CameraMode
from ._node import Node
from ._transform import Transform
from ._texture import load_texture, Texture
from ._color import Color
from ._animation import Animation
from ._prefabs._node2d import Node2D
from ._prefabs._label import Label
from ._prefabs._sprite import Sprite
from ._prefabs._animated_sprite import AnimatedSprite
from . import text
