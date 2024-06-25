from __future__ import annotations as _annotations

from typing import (
    Generator as _Generator,
    Any as _Any
)

from linflex import Vec2 as _Vec2

from ._annotations import (
    NodeType as _NodeType,
    TransformNode as _TransformNode
)


class Transform:
    _transform_instances: dict[int, _TransformNode] = {}

    @classmethod
    def iter_transform_nodes(cls) -> _Generator[_TransformNode, None, None]:
        yield from cls._transform_instances.values()
    
    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs) # type: _TransformNode  # type: ignore[reportAssignmentType]
        Transform._transform_instances[instance.uid] = instance
        instance.position = _Vec2(0, 0)
        return instance # type: ignore

    position: _Vec2
    rotation: float = 0
    z_index: int = 0
    is_top_level: bool = False

    def with_position(self, position: _Vec2, /):
        self.position = position
        return self
    
    def with_rotation(self, rotation: float, /):
        self.rotation = rotation
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
        parent = self.parent # type: ignore
        while parent is not None and isinstance(parent, Transform):
            global_position = parent.position + global_position.rotated(parent.rotation)
            if parent.is_top_level:
                return global_position
            parent = parent.parent # type: ignore
        return global_position
    
    @global_position.setter
    def global_position(self, position: _Vec2) -> None:
        """Sets the node's global position (world space)
        """
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
        parent = self.parent # type: ignore
        while parent is not None and isinstance(parent, Transform):
            global_rotation += parent.rotation
            if parent.is_top_level:
                return global_rotation
            parent = parent.parent # type: ignore
        return global_rotation

    @global_rotation.setter
    def global_rotation(self, rotation: float) -> None:
        """Sets the node's global rotation (world space)
        """
        diff = rotation - self.global_rotation
        self.rotation += diff
    
    def free(self: _TransformNode) -> None:
        del Transform._transform_instances[self.uid]
        super().free()
