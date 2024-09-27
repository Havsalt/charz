from __future__ import annotations as _annotations

from .._node import Node as _Node
from .._components._transform import Transform as _Transform


class Node2D(_Transform, _Node):
    def __str__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + f"#{self.uid}"
            + f":{self.position}"
            + f":{self.rotation}"
            + ")"
        )
