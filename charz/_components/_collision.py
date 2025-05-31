from __future__ import annotations

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
    """

    size: Vec2
    centered: bool = False


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
    disabled: bool = False

    def with_hitbox(self, hitbox: Hitbox, /) -> Self:
        """Chained method to set the hitbox.

        Args:
            hitbox (Hitbox): The hitbox to set.

        Returns:
            Self: Same node instance.
        """
        self.hitbox = hitbox
        return self

    def with_disabled(self, state: bool = True, /) -> Self:
        """Chained method to set the disabled state of the collider.

        Args:
            state (bool): Whether to disable the collider. Defaults to True.

        Returns:
            Self: Same node instance.
        """
        self.disabled = state
        return self

    def get_colliders(self) -> list[ColliderNode]:
        """Get a list of colliders that this node is colliding with.

        This method iterates through all nodes in the `Group.Collider` group and checks
        if this node is colliding with any of them.

        Returns:
            list[ColliderNode]: List of colliders that this node is colliding with.
        """
        assert isinstance(self, ColliderNode)
        nodes_collided_with: list[ColliderNode] = []
        # NOTE: Iterate `dict_values` instead of creating a `list`
        for node in Scene.current.groups[Group.COLLIDER].values():
            if self is node:
                continue
            assert isinstance(node, ColliderNode), (
                f"Node {node} missing 'ColliderComponent'"
            )
            if self.is_colliding_with(node):
                nodes_collided_with.append(node)
        return nodes_collided_with

    def is_colliding(self) -> bool:
        """Check if this node is colliding with any other collider node.

        This method iterates through all nodes in the `Group.Collider` group and checks
        if this node is colliding with any of them.

        Returns:
            bool: Whether this node is colliding with any other collider node.
        """
        assert isinstance(self, ColliderNode)
        for node in Scene.current.groups[Group.COLLIDER].values():
            if self is node:
                continue
            assert isinstance(node, ColliderNode), (
                f"Node {node} missing 'ColliderComponent'"
            )
            if self.is_colliding_with(node):
                return True
        return False

    def is_colliding_with(self, colldier_node: ColliderNode, /) -> bool:
        """Check if this node is colliding with another collider node.

        This method may be overridden in subclasses to implement custom collision logic.
        The custom logic is only used when the call is made from this node.
        This means other colldier nodes will still use their own logic.

        Args:
            colldier_node (ColliderNode): The other collider node to check collision with.

        Returns:
            bool: Whether this node is colliding with the other collider node.
        """
        if self.disabled or colldier_node.disabled:
            return False
        # TODO: Consider `.global_rotation`
        assert isinstance(self, ColliderNode)
        start = self.global_position
        end = self.global_position + self.hitbox.size
        if self.hitbox.centered:
            start -= self.hitbox.size / 2
            end -= self.hitbox.size / 2
        return start <= colldier_node.global_position < end
