from __future__ import annotations

from copy import deepcopy
from typing import Any

from linflex import Vec2
from typing_extensions import Self


class Transform:  # Component (mixin class)
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        if (class_position := getattr(instance, "position", None)) is not None:
            instance.position = deepcopy(class_position)
        else:
            instance.position = Vec2.ZERO
        return instance

    position: Vec2
    rotation: float = 0
    top_level: bool = False

    # TODO: would be nice to figure out @overload with this function
    def with_position(
        self,
        position: Vec2 | None = None,
        /,
        x: float | None = None,
        y: float | None = None,
    ) -> Self:
        if position is None and x is None and y is None:
            raise TypeError(f"not all arguments can be {None} at the same time")
        if position is not None and (x is not None or y is not None):
            raise TypeError(
                "chose either positional argument 'position' "
                "or keyword arguments 'x' and/or 'y', not all three"
            )
        if position is not None:
            self.position = position
        if x is not None:
            self.position.x = x
        if y is not None:
            self.position.y = y
        return self

    # TODO: would be nice to figure out @overload with this function
    def with_global_position(
        self,
        global_position: Vec2 | None = None,
        /,
        x: float | None = None,
        y: float | None = None,
    ) -> Self:
        if global_position is None and x is None and y is None:
            raise TypeError(f"not all arguments can be {None} at the same time")
        if global_position is not None and (x is not None or y is not None):
            raise TypeError(
                "chose either positional argument 'global_position' "
                "or keyword arguments 'x' and/or 'y', not all three"
            )
        if global_position is not None:
            self.global_position = global_position
        if x is not None:
            self.set_global_x(x)
        if y is not None:
            self.set_global_y(y)
        return self

    def with_rotation(self, rotation: float, /) -> Self:
        self.rotation = rotation
        return self

    def with_global_rotation(self, global_rotation: float, /) -> Self:
        self.global_rotation = global_rotation
        return self

    def with_top_level(self, state: bool = True, /) -> Self:
        self.top_level = state
        return self

    def set_global_x(self, x: float, /) -> None:
        diff_x = x - self.global_position.x
        self.position.x += diff_x

    def set_global_y(self, y: float, /) -> None:
        diff_y = y - self.global_position.y
        self.position.y += diff_y

    @property
    def global_position(self) -> Vec2:
        """Returns a copy of the node's global position (in world space)

        `NOTE`: Cannot do `self.global_position.x += 5`,
        use `self.position += 5` instead, as it only adds a relative value

        `NOTE`: Cannot do `self.global_position.x = 42`,
        use `self.set_global_x(42)`

        Returns:
            Vec2: copy of global position
        """
        if self.top_level:
            return self.position.copy()
        global_position = self.position.copy()
        parent = self.parent  # type: ignore
        while isinstance(parent, Transform):
            # check for rotation, since cos(0) and sin(0) produces *approximate* values
            if parent.rotation:
                global_position = parent.position + global_position.rotated(
                    parent.rotation
                )
            else:
                global_position += parent.position
            if parent.top_level:
                return global_position
            parent = parent.parent  # type: ignore
        return global_position

    @global_position.setter
    def global_position(self, position: Vec2) -> None:
        """Sets the node's global position (world space)"""
        diff = position - self.global_position
        self.position += diff

    @property
    def global_rotation(self) -> float:
        """Computes the node's global rotation (world space)

        Returns:
            float: global rotation in radians
        """
        if self.top_level:
            return self.rotation
        global_rotation = self.rotation
        parent = self.parent  # type: ignore
        while isinstance(parent, Transform):
            global_rotation += parent.rotation
            if parent.top_level:
                return global_rotation
            parent = parent.parent  # type: ignore
        return global_rotation

    @global_rotation.setter
    def global_rotation(self, rotation: float) -> None:
        """Sets the node's global rotation (world space)"""
        diff = rotation - self.global_rotation
        self.rotation += diff
