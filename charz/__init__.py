"""
Charz
----

An object oriented terminal game engine

Includes:
- `Engine`
- `Clock`
- `DeltaClock`
- `Screen`
- `Node` (base node)
- `Transform` (component)
- `Vec2` (datastructure from `linflex` package)
- `Texture` (component)
- `Color` (component)
- `ColorValue` (annotation from `colex` package)
- `Sprite` (prefabricated)
"""

from __future__ import annotations as _annotations

__version__ = "0.0.3"
__all__ = [
    "Engine",
    "Clock",
    "DeltaClock",
    "Screen",
    "Node",
    "Transform",
    "Vec2",
    "Texture",
    "Color",
    "ColorValue",
    "Sprite"
]

from linflex import Vec2
from colex import ColorValue

from ._engine import Engine
from ._clock import Clock, DeltaClock
from ._screen import Screen
from ._node import Node
from ._transform import Transform
from ._texture import Texture
from ._color import Color
from ._prefabs._sprite import Sprite
