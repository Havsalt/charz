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
    mode: CameraMode = CameraMode.FIXED

    def set_current(self) -> None:
        Camera.current = self
    
    def as_current(self, state: bool = True):
        if state:
            self.set_current()
            return self
        Camera.current = Camera() # make new default camera
        Camera.current.free() # remove from node count, will still be used as placeholder
        return self

    def is_current(self) -> bool:
        return Camera.current is self
    
    def with_mode(self, mode: CameraMode, /):
        self.mode = mode
        return self


Camera.current = Camera() # initial camera
Camera.current.free() # remove from node count, will still be used as placeholder
