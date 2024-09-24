from __future__ import annotations as _annotations

from copy import deepcopy as _deepcopy
from typing import (
    Generator as _Generator,
    Any as _Any,
    ClassVar as _ClassVar,
)

from linflex import Vec2 as _Vec2

from ._annotations import (
    NodeType as _NodeType,
    TransformNode as _TransformNode,
)


class Transform:
    transform_instances: _ClassVar[dict[int, _TransformNode]] = {}

    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs)  # type: _TransformNode  # type: ignore[reportAssignmentType]
        Transform.transform_instances[instance.uid] = instance
        if (class_position := getattr(instance, "position", None)) is not None:
            instance.position = _deepcopy(class_position)
        else:
            instance.position = _Vec2.ZERO
        return instance  # type: ignore

    position: _Vec2
    rotation: float = 0
    z_index: int = 0
    is_top_level: bool = False

    # TODO: would be nice to figure out @overload with this function
    def with_position(
        self,
        position: _Vec2 | None = None,
        /,
        x: float | None = None,
        y: float | None = None,
    ):
        if position is None and x is None and y is None:
            raise TypeError(f"not all arguments can be {None} at the same time")
        if position is not None and (x is not None or y is not None):
            raise TypeError(
                "chose either positional argument 'position' "
                "or keyword arguments 'x' and/or 'y', not all three"
            )
        if position is not None:
            self.position = position
        if x is not None or y is not None:
            self.position = _Vec2(x or 0, y or 0)
        return self

    # TODO: would be nice to figure out @overload with this function
    def with_global_position(
        self,
        global_position: _Vec2 | None = None,
        /,
        x: float | None = None,
        y: float | None = None,
    ):
        if global_position is None and x is None and y is None:
            raise TypeError(f"not all arguments can be {None} at the same time")
        if global_position is not None and (x is not None or y is not None):
            raise TypeError(
                "chose either positional argument 'global_position' "
                "or keyword arguments 'x' and/or 'y', not all three"
            )
        if global_position is not None:
            self.global_position = global_position
        if x is not None or y is not None:
            self.global_position = _Vec2(x or 0, y or 0)
        return self

    def with_rotation(self, rotation: float, /):
        self.rotation = rotation
        return self
    
    def with_global_rotation(self, global_rotation: float, /):
        self.global_rotation = global_rotation
        return self

    def with_z_index(self, z_index: int, /):
        self.z_index = z_index
        return self

    def as_top_level(self, state: bool = True, /):
        self.is_top_level = state
        return self

    @property
    def global_position(self) -> _Vec2:
        """Computes the node's global position (world space)

        Returns:
            _Vec2: global position
        """
        if self.is_top_level:
            return self.position
        global_position = self.position
        parent = self.parent  # type: ignore
        while parent is not None and isinstance(parent, Transform):
            global_position = parent.position + global_position.rotated(parent.rotation)
            if parent.is_top_level:
                return global_position
            parent = parent.parent  # type: ignore
        return global_position

    @global_position.setter
    def global_position(self, position: _Vec2) -> None:
        """Sets the node's global position (world space)"""
        diff = position - self.global_position
        self.position += diff

    @property
    def global_rotation(self) -> float:
        """Computes the node's global rotation (world space)

        Returns:
            float: global rotation in radians
        """
        if self.is_top_level:
            return self.rotation
        global_rotation = self.rotation
        parent = self.parent  # type: ignore
        while parent is not None and isinstance(parent, Transform):
            global_rotation += parent.rotation
            if parent.is_top_level:
                return global_rotation
            parent = parent.parent  # type: ignore
        return global_rotation

    @global_rotation.setter
    def global_rotation(self, rotation: float) -> None:
        """Sets the node's global rotation (world space)"""
        diff = rotation - self.global_rotation
        self.rotation += diff

    def free(self: _TransformNode) -> None:
        del Transform.transform_instances[self.uid]
        super().free()
