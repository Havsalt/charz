from __future__ import annotations as _annotations

from .._node import Node as _Node
from .._transform import Transform as _Transform
from .._texture import Texture as _Texture
from .._color import Color as _Color


class Sprite(_Color, _Texture, _Transform, _Node): ...
