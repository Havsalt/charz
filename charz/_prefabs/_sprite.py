from __future__ import annotations as _annotations

from .._node import Node as _Node
from .._components._transform import Transform as _Transform
from .._components._texture import Texture as _Texture
from .._components._color import Color as _Color


class Sprite(_Color, _Texture, _Transform, _Node):
    def __str__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + f"#{self.uid}"
            + f":{self.position}"
            + f":{round(self.rotation, 2)}R"
            + f":{'{}x{}'.format(*self.get_texture_size().to_tuple())}"
            + f":{repr(self.color)}"
            + ")"
        )
