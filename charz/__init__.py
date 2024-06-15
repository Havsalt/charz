"""
Charz
----

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
- `Sprite` (prefabricated)
- `Label` (prefabricated)
"""

from __future__ import annotations as _annotations

__version__ = "0.0.4"
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
    "Texture",
    "Color",
    "ColorValue",
    "Sprite",
    "Label"
]

from linflex import Vec2
from colex import ColorValue

from ._engine import Engine
from ._clock import Clock, DeltaClock
from ._screen import Screen
from ._camera import Camera, CameraMode
from ._node import Node
from ._node2d import Node2D
from ._transform import Transform
from ._texture import Texture
from ._color import Color
from ._prefabs._sprite import Sprite
from ._prefabs._label import Label
