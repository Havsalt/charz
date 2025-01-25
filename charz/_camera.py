from __future__ import annotations

from enum import Flag, auto
from typing import ClassVar

from typing_extensions import Self

from ._node import Node
from ._components._transform import Transform


class CameraMode(Flag):
    FIXED = auto()
    CENTERED = auto()
    INCLUDE_SIZE = auto()


class Camera(Transform, Node):
    MODE_FIXED = CameraMode.FIXED
    MODE_CENTERED = CameraMode.CENTERED
    MODE_INCLUDE_SIZE = CameraMode.INCLUDE_SIZE
    current: ClassVar[Camera]
    mode: CameraMode = MODE_FIXED

    def set_current(self) -> None:
        Camera.current = self

    def as_current(self) -> Self:
        self.set_current()
        return self

    def is_current(self) -> bool:
        return Camera.current is self

    def with_mode(self, mode: CameraMode, /) -> Self:
        self.mode = mode
        return self


Camera.current = Camera()  # initial camera
# remove from node count, will still be used as placeholder
Camera.current._free()
