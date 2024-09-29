from __future__ import annotations as _annotations

from dataclasses import dataclass as _dataclass
from copy import deepcopy as _deepcopy
from typing import (
    ClassVar as _ClassVar,
    Any as _Any,
    cast as _cast,
)

from linflex import Vec2
from typing_extensions import Self as _Self

from ._components._transform import Transform as _Transform
from ._annotations import (
    NodeType as _NodeType,
    ColliderNode as _ColliderNode,
)


@_dataclass(kw_only=True)
class Hitbox:
    size: Vec2
    centered = False


class Collider:  # Component (mixin class)
    collider_instances: _ClassVar[dict[int, _ColliderNode]] = {}

    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs)  # type: _ColliderNode  # type: ignore[reportAssignmentType]
        Collider.collider_instances[instance.uid] = instance
        if (class_hitbox := getattr(instance, "hitbox", None)) is not None:
            instance.hitbox = _deepcopy(class_hitbox)
        else:
            instance.hitbox = Hitbox(size=Vec2.ZERO)
        return instance  # type: ignore

    hitbox: Hitbox

    def with_hitbox(self, hitbox: Hitbox, /) -> _Self:
        self.hitbox = hitbox
        return self

    def get_colliders(self) -> list[Collider]:
        self = _cast(_ColliderNode, self)
        colliders: list[Collider] = []
        for node in _Transform.transform_instances.values():
            if isinstance(node, Collider) and node.is_colliding_with(self):
                colliders.append(node)
        return colliders

    def is_colliding_with(self, colldier_node: _ColliderNode, /) -> bool:
        # TODO: consider `.rotation`
        self = _cast(_ColliderNode, self)
        start = self.global_position
        end = self.global_position + self.hitbox.size
        if self.hitbox.centered:
            start -= self.hitbox.size / 2
            end -= self.hitbox.size / 2
        return start <= colldier_node.global_position <= end

    def is_colliding(self) -> bool:
        return bool(self.get_colliders())

    def free(self) -> None:
        self = _cast(_ColliderNode, self)
        del Collider.collider_instances[self.uid]
        super().free()  # type: ignore
