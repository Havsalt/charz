from __future__ import annotations

from functools import wraps
from copy import deepcopy
from enum import Enum, unique, auto
from typing import Any

from charz_core import Self, group

from .._animation import AnimationSet, Animation
from .._grouping import Group


@unique
class PlaybackDirection(Enum):
    FORAWRD = auto()
    BACKWARD = auto()


@group(Group.ANIMATED)
class AnimatedComponent:  # Component (mixin class)
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        if (class_animations := getattr(instance, "animations", None)) is not None:
            instance.animations = deepcopy(class_animations)
        else:
            instance.animations = AnimationSet()
        return instance

    animations: AnimationSet
    current_animation: Animation | None = None
    repeat: bool = False
    is_playing: bool = False
    _frame_index: int = 0
    _playback_direction: PlaybackDirection = PlaybackDirection.FORAWRD
    _is_on_last_frame: bool = False

    def with_animations(self, /, **animations: Animation) -> Self:
        # NOTE: Additive
        for animation_name, animation in animations.items():
            setattr(self.animations, animation_name, animation)
        return self

    def with_animation(
        self,
        animation_name: str,
        animation: Animation,
        /,
    ) -> Self:
        # NOTE: Additive
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
            raise ValueError(f"Animation not found: '{animation_name}'")
        self.current_animation = getattr(self.animations, animation_name)
        self.is_playing = True
        self._playback_direction = PlaybackDirection.FORAWRD
        self._is_on_last_frame = False
        self._frame_index = 0
        # The actual logic of playing the animation
        # is handled in `.update_animation`

    def play_backwards(self, animation_name: str, /) -> None:
        if not hasattr(self.animations, animation_name):
            raise ValueError(f"Animation not found: '{animation_name}'")
        self.current_animation = getattr(self.animations, animation_name)
        assert isinstance(self.current_animation, Animation)
        self.is_playing = True
        self._playback_direction = PlaybackDirection.BACKWARD
        self._is_on_last_frame = False
        self._frame_index = len(self.current_animation.frames) - 1
        # The actual logic of playing the animation
        # is handled in `.update_animation`

    def update_animation(self) -> None:
        if self.current_animation is None:
            self.is_playing = False
            return

        self.texture = self.current_animation.frames[self._frame_index]
        frame_count = len(self.current_animation.frames)
        index_change = 1 if self._playback_direction is PlaybackDirection.FORAWRD else -1

        if self.is_playing and self.repeat and self._is_on_last_frame:
            self._is_on_last_frame = False
            first_index = (
                0
                if self._playback_direction is PlaybackDirection.FORAWRD
                else frame_count - 1
            )
            self._frame_index = first_index
            return
        # Progress frame index
        self._frame_index = min(
            frame_count - 1,
            max(
                0,
                self._frame_index + index_change,
            ),
        )
        last_index = (
            frame_count - 1
            if self._playback_direction is PlaybackDirection.FORAWRD
            else 0
        )
        # State variable to ensure last frame is shown when `.repeat` is `True`
        if self._frame_index == last_index:
            if self.repeat:
                self._is_on_last_frame = True
            else:
                self.is_playing = False
