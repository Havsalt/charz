from __future__ import annotations as _annotations

from enum import (
    IntEnum as _IntEnum,
    auto as _auto,
)
from typing import ClassVar as _ClassVar

from ._node import Node as _Node
from ._transform import Transform as _Transform


class CameraMode(_IntEnum):
    FIXED = 0
    CENTERED = _auto()
    INCLUDE_SIZE = _auto()

    def __or__(self, other: CameraMode) -> CameraMode:
        # NOTE: result may not be a member of 'CameraMode', but instead an 'int'.
        # combine any 'CameraMode', where any value that is not bound to a variant,
        # will in fact be an 'int', but we treat it like a 'CameraMode' that was combined
        if isinstance(other, CameraMode):
            new_value = self.value | other.value
            if new_value in CameraMode._value2member_map_:
                return CameraMode(new_value)
            return new_value  # type: ignore
        return NotImplemented


class Camera(_Transform, _Node):
    current: _ClassVar[Camera]
    mode: CameraMode = CameraMode.FIXED

    def set_current(self) -> None:
        Camera.current = self

    def as_current(self, state: bool = True):
        if state:
            self.set_current()
            return self
        Camera.current = Camera()  # make new default camera
        Camera.current.free()  # remove from node count, will still be used as placeholder
        return self

    def is_current(self) -> bool:
        return Camera.current is self

    def with_mode(self, mode: CameraMode, /):
        self.mode = mode
        return self


Camera.current = Camera()  # initial camera
Camera.current.free()  # remove from node count, will still be used as placeholder
