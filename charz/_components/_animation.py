from __future__ import annotations as _annotations

from types import SimpleNamespace as _SimpleNamespace
from functools import wraps as _wraps
from pathlib import Path as _Path
from copy import deepcopy as _deepcopy
from typing import (
    Any as _Any,
    ClassVar as _ClassVar,
    cast as _cast,
)

from typing_extensions import Self as _Self

from ._texture import load_texture as _load_texture
from .._annotations import (
    T as _T,
    NodeType as _NodeType,
    AnimatedNode as _AnimatedNode,
)


class Animation:
    __slots__ = ("frames",)
    frames: list[list[str]]

    def __init__(self, animation_path: _Path | str, /) -> None:
        # fmt: off
        frame_directory = (
            _Path.cwd()
            .joinpath(str(animation_path))
            .iterdir()
        )
        # fmt: on
        self.frames = list(map(_load_texture, frame_directory))


class AnimationMapping(_SimpleNamespace):
    def __init__(self, **animations: Animation) -> None:
        super().__init__(**animations)

    def __getattribute__(self, name: str) -> Animation:
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Animation) -> None:
        return super().__setattr__(name, value)

    def get(self, animation_name: str, default: _T = None) -> Animation | _T:
        return getattr(self, animation_name, default)

    def update(self, animations: dict[str, Animation]) -> None:
        for name, animation in animations.items():
            setattr(self, name, animation)


# TODO: add `.play_backwards` attribute or method
# TODO: ensure last frame was rendered before `.is_playing = False`,
#       because a loop checking if it should replay the animations will
#       reset it back to the first frame before the last one is displayed
class Animated:  # Component (mixin class)
    animated_instances: _ClassVar[dict[int, _AnimatedNode]] = {}

    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs)  # type: _AnimatedNode  # type: ignore
        Animated.animated_instances[instance.uid] = instance
        if (class_animations := getattr(instance, "animations", None)) is not None:
            instance.animations = _deepcopy(class_animations)
        else:
            instance.animations = AnimationMapping()

        # inject `._wrapped_update_animated()` into `.update()`
        def update_method_factory(instance: _AnimatedNode, bound_update):  # noqa: ANN001 ANN202
            @_wraps(bound_update)
            def new_update_method(delta: float) -> None:
                bound_update(delta)  # TODO: swap order will fix rendering??
                instance._wrapped_update_animated(delta)

            return new_update_method

        instance.update = update_method_factory(instance, instance.update)
        return instance  # type: ignore

    animations: AnimationMapping
    current_animation: Animation | None = None
    is_playing: bool = False
    _frame_index: int = 0

    def with_animations(self, /, **animations: Animation) -> _Self:
        self.animations.update(animations)
        return self

    def with_animation(
        self,
        animation_name: str,
        animation: Animation,
        /,
    ) -> _Self:
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

    def free(self) -> None:
        self = _cast(_AnimatedNode, self)
        del Animated.animated_instances[self.uid]
        super().free()  # type: ignore
