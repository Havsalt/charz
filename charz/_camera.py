from __future__ import annotations

from enum import IntEnum, auto
from typing import ClassVar

from typing_extensions import Self

from ._node import Node
from ._components._transform import Transform


class CameraMode(IntEnum):
    FIXED = 0
    CENTERED = auto()
    INCLUDE_SIZE = auto()

    def __or__(self, other: CameraMode) -> CameraMode:
        """Merge two CameraMode values into a new CameraMode value

        NOTE: Result may not be a member of `CameraMode`, but instead an `int`.
        Combine any `CameraMode`, where any value that is not bound to a variant,
        will in fact be an `int`, but we treat it like a `CameraMode` that was combined

        Args:
            other (CameraMode): other CameraMode value to merge with

        Returns:
            CameraMode: new combined CameraMode value
        """
        if isinstance(other, CameraMode):
            new_value = self.value | other.value
            if new_value in CameraMode._value2member_map_:
                return CameraMode(new_value)
            return new_value  # type: ignore
        raise TypeError(
            f"unsupported operand type(s) for |: 'CameraMode' and '{type(other)}'"
        )


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
