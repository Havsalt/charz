from __future__ import annotations as _annotations

from types import SimpleNamespace as _SimpleNamespace
from functools import wraps as _wraps
from pathlib import Path as _Path
from typing import (
    Generic as _Generic,
    Generator as _Generator,
    Any as _Any,
    ClassVar as _ClassVar
)

from ._texture import load_texture as _load_texture
from ._annotations import (
    T as _T,
    NodeType as _NodeType,
    AnimatedNode as _AnimatedNode
)


class Animation:
    __slots__ = ("frames",)
    frames: list[list[str]]

    def __init__(self, animation_path: _Path | str, /) -> None:
        self.frames = [
            _load_texture(frame_path)
            for frame_path in (
                _Path.cwd()
                .joinpath(str(animation_path))
                .iterdir()
            )
        ]


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


class Animated: # Component (mixin class)
    _animated_instances: _ClassVar[dict[int, _AnimatedNode]] = {}

    @classmethod
    def iter_animated_nodes(cls) -> _Generator[_AnimatedNode, None, None]:
        yield from cls._animated_instances.values()

    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs) # type: _AnimatedNode  # type: ignore[reportAssignmentType]
        Animated._animated_instances[instance.uid] = instance
        instance.animations = AnimationMapping()

        # inject `._wrapped_update_animated()` into `.update()`
        def update_method_factory(instance: _AnimatedNode, bound_update):
            @_wraps(bound_update)
            def new_update_method(delta: float) -> None:
                bound_update(delta)
                instance._wrapped_update_animated(delta)
            return new_update_method

        instance.update = update_method_factory(instance, instance.update)
        return instance # type: ignore

    animations: AnimationMapping
    current_animation: Animation | None = None
    is_playing: bool = False
    _frame_index: int = 0

    def with_animations(self, /, **animations: Animation):
        self.animations.update(animations)
        return self
    
    def with_animation(
        self,
        animation_name: str,
        animation: Animation,
        /
    ):
        setattr(self.animations, animation_name, animation)
        return self
    
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
    
    def free(self: _AnimatedNode) -> None:
        del Animated._animated_instances[self.uid]
        super().free()
