from __future__ import annotations

from types import SimpleNamespace
from functools import wraps
from pathlib import Path
from copy import deepcopy
from typing import Any, ClassVar

from typing_extensions import Self

from ._texture import load_texture
from .._annotations import T, AnimatedNode


class Animation:
    __slots__ = ("frames",)

    def __init__(self, animation_path: Path | str, /) -> None:
        # fmt: off
        frame_directory = (
            Path.cwd()
            .joinpath(str(animation_path))
            .iterdir()
        )
        # fmt: on
        self.frames = list(map(load_texture, frame_directory))

    def __repr__(self) -> str:
        # should never be empty, but if the programmer did it, show empty frame count
        if not self.frames:
            return f"{self.__class__.__name__}(▦!:N/A->N/A)"
        longest = 0
        shortest = 0
        tallest = 0
        lowest = 0
        # these are used as temporary variables in loop
        local_longest = 0
        local_shortest = 0
        local_tallest = 0
        local_lowest = 0
        for frame in self.frames:
            # compare all time best against best results per iteration
            if not frame:  # allow empty frame
                continue
            elif not any(frame):  # allow frame with empty lines
                continue
            local_longest = len(max(frame, key=len))
            longest = max(local_longest, longest)
            local_tallest = len(frame)
            tallest = max(local_tallest, tallest)
            local_shortest = len(min(frame, key=len))
            shortest = min(local_shortest, shortest)
            local_lowest = min(local_lowest, shortest)
        return (
            self.__class__.__name__
            + "("
            + f"▦{len(self.frames)}"
            + f":{shortest}x{lowest}"
            + f"->{longest}x{tallest}"
            + ")"
        )


class AnimationMapping(SimpleNamespace):
    def __init__(self, **animations: Animation) -> None:
        super().__init__(**animations)

    def __getattribute__(self, name: str) -> Animation:
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Animation) -> None:
        return super().__setattr__(name, value)

    def get(self, animation_name: str, default: T = None) -> Animation | T:
        return getattr(self, animation_name, default)

    def update(self, animations: dict[str, Animation]) -> None:
        for name, animation in animations.items():
            setattr(self, name, animation)


# TODO: add `.play_backwards` attribute or method
# TODO: ensure last frame was rendered before `.is_playing = False`,
#       because a loop checking if it should replay the animations will
#       reset it back to the first frame before the last one is displayed
class Animated:  # Component (mixin class)
    animated_instances: ClassVar[dict[int, AnimatedNode]] = {}

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        Animated.animated_instances[instance.uid] = instance  # type: ignore
        if (class_animations := getattr(instance, "animations", None)) is not None:
            instance.animations = deepcopy(class_animations)
        else:
            instance.animations = AnimationMapping()

        # inject `._wrapped_update_animated()` into `.update()`
        def update_method_factory(instance: AnimatedNode, bound_update):  # noqa: ANN001 ANN202
            @wraps(bound_update)
            def new_update_method(delta: float) -> None:
                bound_update(delta)  # TODO: swap order will fix rendering??
                instance._wrapped_update_animated(delta)

            return new_update_method

        instance.update = update_method_factory(instance, instance.update)  # type: ignore
        return instance  # type: ignore

    animations: AnimationMapping
    current_animation: Animation | None = None
    is_playing: bool = False
    _frame_index: int = 0

    def with_animations(self, /, **animations: Animation) -> Self:
        self.animations.update(animations)
        return self

    def with_animation(
        self,
        animation_name: str,
        animation: Animation,
        /,
    ) -> Self:
        self.add_animation(animation_name, animation)
        return self

    def add_animation(
        self,
        animation_name: str,
        animation: Animation,
        /,
    ) -> None:
        setattr(self.animations, animation_name, animation)

    def play(self, animation_name: str, /) -> None:
        self.current_animation = self.animations.get(animation_name, None)
        self.is_playing = True
        self._frame_index = 0
        # the actual logic of playing the animation is handled in `.update(...)`

    def _wrapped_update_animated(self, _delta: float) -> None:
        if self.current_animation is None:
            self.is_playing = False
            return
        self.texture = self.current_animation.frames[self._frame_index]
        frame_count = len(self.current_animation.frames)
        self._frame_index = min(self._frame_index + 1, frame_count - 1)
        if self._frame_index == frame_count - 1:
            self.is_playing = False

    def _free(self) -> None:
        del Animated.animated_instances[self.uid]  # type: ignore
        super()._free()  # type: ignore
