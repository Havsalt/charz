from __future__ import annotations

from math import cos, sin
from dataclasses import dataclass
from copy import deepcopy
from typing import Any

from charz_core import Scene, Vec2, Self, group

from .._grouping import Group
from .._annotations import ColliderNode


@dataclass(kw_only=True)
class Hitbox:
    """Hitbox dataclass for collision shape data.

    Attributes:
        `size`: `Vec2` - Width and height of the hitbox.
        `centered`: `bool` - Whether hitbox is centered around the node's global position.
            Defaults to `False`, meaning the hitbox starts at the node's position,
            and expanding to the right and downwards.
        `disabled`: bool = False
        `margin`: `float` - Inverse margin around the hitbox for collision detection.
    """

    size: Vec2
    centered: bool = False
    disabled: bool = False
    margin: float = 1.0


@group(Group.COLLIDER)
class ColliderComponent:  # Component (mixin class)
    """`ColliderComponent` mixin class for node.

    Assign this component to a node to enable collision detection.
    All other collider components will then do collision detection against this node,
    when `is_colliding` and `get_colliders` is called.

    Attributes:
        `hitbox`: `Hitbox` - The hitbox data for collision detection.
        `disabled`: `bool` - Whether the collider is disabled.

    Methods:
        `get_colliders`
        `is_colliding`
        `is_colliding_with`
    """

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        if (class_hitbox := getattr(instance, "hitbox", None)) is not None:
            instance.hitbox = deepcopy(class_hitbox)
        else:
            instance.hitbox = Hitbox(size=Vec2.ZERO)
        return instance

    hitbox: Hitbox

    def with_hitbox(self, hitbox: Hitbox, /) -> Self:
        """Chained method to set the hitbox.

        Args:
            hitbox (Hitbox): The hitbox to set.

        Returns:
            Self: Same node instance.
        """
        self.hitbox = hitbox
        return self

    def get_colliders(self) -> list[ColliderNode]:
        """Get a list of colliders that this node is colliding with.

        This method iterates through all nodes in the `Group.Collider` group and checks
        if this node is colliding with any of them.

        Returns:
            list[ColliderNode]: List of colliders that this node is colliding with.
        """
        assert isinstance(self, ColliderComponent)
        nodes_collided_with: list[ColliderNode] = []
        # NOTE: Iterate `dict_values` instead of creating a `list` for speed
        for node in Scene.current.groups[Group.COLLIDER].values():
            if self is node:
                continue
            # Ignoring incorrect type because group `Group.Collider`
            # should only contain `ColliderNode` instances
            if self.is_colliding_with(node):  # type: ignore
                nodes_collided_with.append(node)  # type: ignore
        return nodes_collided_with

    def is_colliding(self) -> bool:
        """Check if this node is colliding with any other collider node.

        This method iterates through all nodes in the `Group.Collider` group and checks
        if this node is colliding with any of them.

        Returns:
            bool: Whether this node is colliding with any other collider node.
        """
        assert isinstance(self, ColliderComponent)
        for node in Scene.current.groups[Group.COLLIDER].values():
            if self is node:
                continue
            # Ignoring incorrect type because group `Group.Collider`
            # should only contain `ColliderNode` instances
            if self.is_colliding_with(node):  # type: ignore
                return True
        return False

    def is_colliding_with(self, collider_node: ColliderNode, /) -> bool:
        """Check if this node is colliding with another collider node.

        Uses SAT (Separating Axis Theorem).

        `NOTE` Does not yet fully support rotated hitboxes.

        Args:
            collider_node (ColliderNode): The other collider node to check collision with.

        Returns:
            bool: Whether this node is colliding with the other collider node.
        """
        if self.hitbox.disabled or collider_node.hitbox.disabled:
            return False

        corners_a = self._get_corners(self)  # type: ignore
        corners_b = self._get_corners(collider_node)

        # Axes to test: x and y
        axes = [Vec2(1, 0), Vec2(0, 1)]

        for axis in axes:
            min_a, max_a = self._get_projection_range(corners_a, axis)
            min_b, max_b = self._get_projection_range(corners_b, axis)
            # Hitbox margin is negative space inside the hitbox,
            # extending from the edges
            if (
                max_a - self.hitbox.margin < min_b
                or max_b - collider_node.hitbox.margin < min_a
            ):
                return False  # Separating axis found

        return True  # No separating axis found, collision detected

    @staticmethod
    def _get_corners(node: ColliderNode) -> list[Vec2]:
        global_position = node.global_position
        global_rotation = node.global_rotation
        size = node.hitbox.size

        # Center the hitbox if needed
        if node.hitbox.centered:
            global_position = global_position - size / 2

        # Define corners relative to position
        corners = [
            Vec2(0, 0),
            Vec2(size.x, 0),
            Vec2(size.x, size.y),
            Vec2(0, size.y),
        ]

        # Rotate corners around the hitbox center
        if global_rotation != 0.0:
            center = global_position + size / 2
            rotated = []
            for corner in corners:
                relative = global_position + corner - center
                rotated_corner = (
                    Vec2(
                        relative.x * cos(global_rotation)
                        - relative.y * sin(global_rotation),
                        relative.x * sin(global_rotation)
                        + relative.y * cos(global_rotation),
                    )
                    + center
                )
                rotated.append(rotated_corner)
            return rotated
        else:
            return [global_position + corner for corner in corners]

    @staticmethod
    def _get_projection_range(corners: list[Vec2], axis: Vec2) -> tuple[float, float]:
        projections = [corner.dot(axis) for corner in corners]
        return min(projections), max(projections)
