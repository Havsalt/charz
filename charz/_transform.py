from __future__ import annotations as _annotations

from linflex import Vec2 as _Vec2


class Transform:
    position: _Vec2
    rotation: float

    def get_global_position(self) -> _Vec2:
        """Computes the node's global position (world space)

        Returns:
            _Vec2: global position
        """
        global_position = self.position
        parent = self.parent # type: ignore
        while parent is not None and isinstance(parent, Transform):
            global_position = parent.position + global_position.rotated(parent.rotation)
            parent = parent.parent # type: ignore
        return global_position
    
    def set_global_position(self, position: _Vec2) -> None:
        """Sets the node's global position (world space)
        """
        diff = position - self.get_global_position()
        self.position += diff
    
    def get_global_rotation(self) -> float:
        """Computes the node's global rotation (world space)

        Returns:
            float: global rotation in radians
        """
        global_rotation = self.rotation
        parent = self.parent # type: ignore
        while parent is not None and isinstance(parent, Transform):
            global_rotation += parent.rotation
            parent = parent.parent # type: ignore
        return global_rotation

    def set_global_rotation(self, rotation: float) -> None:
        """Sets the node's global rotation (world space)
        """
        diff = rotation - self.get_global_rotation()
        self.rotation += diff
