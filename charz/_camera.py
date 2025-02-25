from __future__ import annotations

from enum import Flag, auto

from linflex import Vec2
from typing_extensions import Self

from ._node import Node, NodeMixinSorter
from ._components._transform import Transform


class CameraMode(Flag):
    FIXED = auto()
    CENTERED = auto()
    INCLUDE_SIZE = auto()


class CameraClassAttributes(NodeMixinSorter):
    MODE_FIXED: CameraMode = CameraMode.FIXED
    MODE_CENTERED: CameraMode = CameraMode.CENTERED
    MODE_INCLUDE_SIZE: CameraMode = CameraMode.INCLUDE_SIZE
    _current: Camera

    @property
    def current(self) -> Camera:
        if not hasattr(self, "_current"):
            self._current = Camera()  # Create default camera if none exists
        return self._current

    @current.setter
    def current(self, new: Camera | None) -> None:
        if new is None:
            self._current = Camera()
        else:
            self._current = new


class Camera(Transform, Node, metaclass=CameraClassAttributes):
    mode: CameraMode = CameraMode.FIXED

    def __init__(
        self,
        parent: Node | None = None,
        *,
        process_priority: int | None = None,
        position: Vec2 | None = None,
        rotation: float | None = None,
        top_level: bool | None = None,
        mode: CameraMode | None = None,
        current: bool | None = False,
    ) -> None:
        if parent is not None:
            self.parent = parent
        if process_priority is not None:
            self.process_priority = process_priority
        if position is not None:
            self.position = position
        if rotation is not None:
            self.rotation = rotation
        if top_level is not None:  # `bool` and `None` check combined
            self.top_level = top_level
        if mode is not None:
            self.mode = mode
        if current:  # `bool` and `None` check combined
            self.set_current()

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
