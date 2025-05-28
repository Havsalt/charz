from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy
from typing import Any

from charz_core import Scene, Vec2, Self, group

from .._grouping import Group
from .._annotations import ColliderNode


@dataclass(kw_only=True)
class Hitbox:
    size: Vec2
    centered: bool = False


@group(Group.COLLIDER)
class ColliderComponent:  # Component (mixin class)
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
        self.hitbox = hitbox
        return self

    def with_disabled(self, state: bool = True, /) -> Self:
        self.disabled = state
        return self

    def get_colliders(self) -> list[ColliderNode]:
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
