from __future__ import annotations

from functools import wraps
from copy import deepcopy
from enum import Enum, unique, auto
from typing import Any

from charz_core import Self

from .._animation import AnimationSet, Animation
from .._annotations import AnimatedNode


@unique
class PlaybackDirection(Enum):
    FORAWRD = auto()
    BACKWARD = auto()


class Animated:  # Component (mixin class)
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        if (class_animations := getattr(instance, "animations", None)) is not None:
            instance.animations = deepcopy(class_animations)
        else:
            instance.animations = AnimationSet()

        # inject `._wrapped_update_animated()` into `.update()`
        def update_method_factory(instance: AnimatedNode, bound_update):  # noqa: ANN001 ANN202
            @wraps(bound_update)
            def new_update_method(delta: float) -> None:
                bound_update(delta)  # TODO: swap order will fix rendering??
                instance._wrapped_update_animated(delta)

            return new_update_method

        instance.update = update_method_factory(instance, instance.update)  # type: ignore
        return instance  # type: ignore

    animations: AnimationSet
    current_animation: Animation | None = None
    repeat: bool = False
    is_playing: bool = False
    _frame_index: int = 0
    _playback_direction: PlaybackDirection = PlaybackDirection.FORAWRD
    _is_on_last_frame: bool = False

    def with_animations(self, /, **animations: Animation) -> Self:
        # NOTE: additive
        for animation_name, animation in animations.items():
            setattr(self.animations, animation_name, animation)
        return self

    def with_animation(
        self,
        animation_name: str,
        animation: Animation,
        /,
    ) -> Self:
        # NOTE: additive
        self.add_animation(animation_name, animation)
        return self

    def with_repeat(self, state: bool = True, /) -> Self:
        self.repeat = state
        return self

    def add_animation(
        self,
        animation_name: str,
        animation: Animation,
        /,
    ) -> None:
        setattr(self.animations, animation_name, animation)

    def play(self, animation_name: str, /) -> None:
        if not hasattr(self.animations, animation_name):
            raise ValueError(f"animation not found: '{animation_name}'")
        self.current_animation = getattr(self.animations, animation_name)
        self.is_playing = True
        self._is_on_last_frame = False
        self._playback_direction = PlaybackDirection.FORAWRD
        self._frame_index = 0
        # the actual logic of playing the animation
        # is handled in `_wrapped_update_animated`

    def play_backwards(self, animation_name: str, /) -> None:
        if not hasattr(self.animations, animation_name):
            raise ValueError(f"animation not found: '{animation_name}'")
        self.current_animation = getattr(self.animations, animation_name)
        assert isinstance(self.current_animation, Animation)
        self.is_playing = True
        self._is_on_last_frame = False
        self._playback_direction = PlaybackDirection.BACKWARD
        self._frame_index = len(self.current_animation.frames) - 1
        # the actual logic of playing the animation
        # is handled in `_wrapped_update_animated`

    def _wrapped_update_animated(self, _delta: float) -> None:
        if self.current_animation is None:
            self.is_playing = False
            return

        self.texture = self.current_animation.frames[self._frame_index]
        frame_count = len(self.current_animation.frames)
        # using `min` and `max` instead of `clamp`
        # for better linting (`int` instead of `int | float`)
        index_change = 1 if self._playback_direction is PlaybackDirection.FORAWRD else -1
        self._frame_index = min(
            frame_count - 1,
            max(
                0,
                self._frame_index + index_change,
            ),
        )

        if self._is_on_last_frame:
            if self.repeat:
                self._frame_index = 0
                self._is_on_last_frame = False
            else:
                self.is_playing = False

        last_index = (
            frame_count - 1
            if self._playback_direction is PlaybackDirection.FORAWRD
            else 0
        )
        # state variable to ensure last frame is shown
        if self._frame_index == last_index:
            self._is_on_last_frame = True
