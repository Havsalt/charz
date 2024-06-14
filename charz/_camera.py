from __future__ import annotations as _annotations

from enum import IntEnum as _IntEnum, auto as _auto

from ._node import Node as _Node
from ._transform import Transform as _Transform


class CameraMode(_IntEnum):
    FIXED = 0
    CENTERED = _auto()
    FOLLOW = _auto()
    INCLUDE_SIZE = _auto()


class Camera(_Transform, _Node):
    current: Camera

    def set_current(self) -> None:
        Camera.current = self
    
    def as_current(self):
        self.set_current()
        return self

    def is_current(self) -> bool:
        return Camera.current is self


Camera.current = Camera() # initial camera
