from __future__ import annotations

from copy import deepcopy
from enum import Enum, unique, auto
from typing import Any

from charz_core import Self, group, clamp

from .._animation import AnimationSet, Animation
from .._grouping import Group


@unique
class PlaybackDirection(Enum):
    FORAWRD = auto()
    BACKWARD = auto()


@group(Group.ANIMATED)
class AnimatedComponent:  # Component (mixin class)
    """`AnimatedComponent` mixin class for node.

    It provides animation controls,
    and enables the node to manage and play animations defined in `AnimationSet`.

    Attributes:
        `animations`: `AnimationSet` - Collection of named animations.
        `current_animation`: `Animation | None` - Currently active (or paused) animation.
        `repeat`: `bool` - Whether the animation should loop.
        `is_playing`: `bool` - Whether the animation is currently playing.

    Methods:
        `add_animation`
        `play`
        `play_backwards`
        `update_animation`
    """

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
        """Chained method to add multiple animations.

        Args:
            animations (**Animation): Named animations as keyword arguments.

        Returns:
            Self: Same node instance.
        """
        for animation_name, animation in animations.items():
            setattr(self.animations, animation_name, animation)
        return self

    def with_animation(
        self,
        animation_name: str,
        animation: Animation,
        /,
    ) -> Self:
        """Chained method to add a single animation.

        Args:
            animation_name (str): Name of the animation.
            animation (Animation): Animation instance to add.

        Returns:
            Self: Same node instance.
        """
        self.add_animation(animation_name, animation)
        return self

    def with_repeat(self, state: bool = True, /) -> Self:
        """Chained method to set the repeat state of the animation.

        Args:
            state (bool): Whether the animation should repeat. Defaults to `True`.
        """
        self.repeat = state
        return self

    def add_animation(
        self,
        animation_name: str,
        animation: Animation,
        /,
    ) -> None:
        """Add an animation to the node.

        Args:
            animation_name (str): Name of the animation.
            animation (Animation): Animation instance to add.
        """
        setattr(self.animations, animation_name, animation)

    def play(self, animation_name: str, /) -> None:
        """Play an animation by its name.

        Args:
            animation_name (str): Name of the animation to play.

        Raises:
            ValueError: If the animation with the given name does not exist.
        """
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
        """Play an animation in reverse by its name.

        Args:
            animation_name (str): Name of the animation to play in reverse.

        Raises:
            ValueError: If the animation with the given name does not exist.
        """
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

    def progress_animation(self) -> None:
        """Progress `1` frame of current animation.

        Called by a frame task, which is found in `Scene.frame_tasks`.
        """
        if self.current_animation is None:
            self.is_playing = False
            return

        # Change texture to the current frame
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
        self._frame_index = clamp(
            self._frame_index + index_change,
            0,
            frame_count - 1,
        )
        # Check if hit end of animation, last frame index
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
