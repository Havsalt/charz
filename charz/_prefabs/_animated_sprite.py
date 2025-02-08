from __future__ import annotations

from colex import ColorValue
from linflex import Vec2

from .._node import Node

from .._components._animation import Animated, AnimationSet
from ._sprite import Sprite


class AnimatedSprite(Animated, Sprite):
    def __init__(
        self,
        parent: Node | None = None,
        *,
        process_priority: int | None = None,
        position: Vec2 | None = None,
        rotation: float | None = None,
        top_level: bool | None = None,
        texture: list[str] | None = None,
        visible: bool | None = None,
        centered: bool | None = None,
        z_index: int | None = None,
        transparency: str | None = None,
        color: ColorValue | None = None,
        animations: AnimationSet | None = None,
    ) -> None:
        super().__init__(
            parent=parent,
            process_priority=process_priority,
            position=position,
            rotation=rotation,
            top_level=top_level,
            texture=texture,
            visible=visible,
            centered=centered,
            z_index=z_index,
            transparency=transparency,
            color=color,
        )
        if animations is not None:
            self.animations = animations
