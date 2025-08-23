from __future__ import annotations

from colex import ColorValue
from charz_core import Node, Vec2

from .._animation import AnimationSet
from .._components._animated import AnimatedComponent
from ._sprite import Sprite
from .._annotations import Char


class AnimatedSprite(AnimatedComponent, Sprite):
    """`AnimatedSprite` node with multiple textures packed into animations.

    It inherits from `AnimatedComponent` and `Sprite`, allowing it to
    play animations defined in its `AnimationSet, while also being a sprite
    with a texture, position, rotation, and other visual properties.

    Example:

    The paths are relative to the project root,
    unless an animation directory is set in `AssetLoader`.
    See `Animation` for more options when loading.

    ```python
    from charz import AnimatedSprite, AnimationSet, Animation

    class MyAnimatedGoblin(AnimatedSprite):
        animations = AnimationSet(
            Idle=Animation("path/to/idle-animation-folder"),
            Attack=Animation("goblin/attack"),
            AttackLeft=Animation("goblin/attack", flip_h=True),
            Flee=Animation("goblin/attack", reverse=True),
        )
    ```
    """

    def __init__(
        self,
        parent: Node | None = None,
        *,
        position: Vec2 | None = None,
        rotation: float | None = None,
        top_level: bool | None = None,
        texture: list[str] | None = None,
        visible: bool | None = None,
        centered: bool | None = None,
        z_index: int | None = None,
        transparency: Char | None = None,
        color: ColorValue | None = None,
        animations: AnimationSet | None = None,
        repeat: bool | None = None,
    ) -> None:
        Sprite.__init__(
            self,
            parent=parent,
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
        if repeat is not None:
            self.repeat = repeat

    def __repr__(self) -> str:
        visual_frame_sizes: list[str] = []
        animation_count = len(self.animations.__dict__)
        if animation_count:
            for animation in self.animations.__dict__.values():
                visual_frame_size = f"{0}x{1}->{2}x{3}".format(
                    *animation.get_smallest_frame_dimensions(),
                    *animation.get_largest_frame_dimensions(),
                )
                visual_frame_sizes.append(visual_frame_size)
        else:
            visual_frame_sizes.append("N/A")

        return (
            self.__class__.__name__
            + "("
            + f"#{self.uid}"
            + f":{round(self.position, 2)}"
            + f":{round(self.rotation, 2)}R"
            + f":{'{}x{}'.format(*self.get_texture_size())}"
            + f":{repr(self.color)}"
            + f":A={animation_count},"
            + ",".join(visual_frame_sizes)
            + ")"
        )
