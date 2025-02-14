from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy
from typing import ClassVar, Any, cast

from linflex import Vec2
from typing_extensions import Self

from .._components._transform import Transform
from .._annotations import ColliderNode


@dataclass(kw_only=True)
class Hitbox:
    size: Vec2
    centered: bool = False


class Collider:  # Component (mixin class)
    collider_instances: ClassVar[dict[int, ColliderNode]] = {}

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        Collider.collider_instances[instance.uid] = instance  # type: ignore
        if (class_hitbox := getattr(instance, "hitbox", None)) is not None:
            instance.hitbox = deepcopy(class_hitbox)
        else:
            instance.hitbox = Hitbox(size=Vec2.ZERO)
        return instance

    hitbox: Hitbox

    def with_hitbox(self, hitbox: Hitbox, /) -> Self:
        self.hitbox = hitbox
        return self

    def get_colliders(self) -> list[Collider]:
        self = cast(ColliderNode, self)
        colliders: list[Collider] = []
        for node in Transform.transform_instances.values():
            if self is node:
                continue
            # NOTE: might swap who the `.is_colliding_with(...)` is checked on
            if isinstance(node, Collider) and node.is_colliding_with(self):
                colliders.append(node)
        return colliders

    def is_colliding_with(self, colldier_node: ColliderNode, /) -> bool:
        # TODO: consider `.global_rotation`
        self = cast(ColliderNode, self)
        start = self.global_position
        end = self.global_position + self.hitbox.size
        if self.hitbox.centered:
            start -= self.hitbox.size / 2
            end -= self.hitbox.size / 2
        return start <= colldier_node.global_position < end

    def is_colliding(self) -> bool:
        return bool(self.get_colliders())

    def _free(self) -> None:
        del Collider.collider_instances[self.uid]  # type: ignore
        super()._free()  # type: ignore
