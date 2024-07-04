from __future__ import annotations as _annotations

from functools import wraps as _wraps
from typing import (
    Any as _Any,
    Callable as _Callable
)

from ._clock import (
    Clock as _Clock,
    DeltaClock as _DeltaClock
)
from ._screen import Screen as _Screen
from ._node import Node as _Node
from ._annotations import EngineType as _EngineType


class _EngineMixinSortMeta(type):
    """Engine metaclass for initializing `Engine` subclass after other `mixin` classes
    """
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, object]):
        sorter = lambda base: isinstance(base, Engine)
        sorted_bases = tuple(sorted(bases, key=sorter))
        new_type = super().__new__(cls, name, sorted_bases, attrs)
        return new_type


class _EngineInitWrapperMeta(type):
    """Wraps the `__init__` method with extra logic
    """
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, object]):
        new_type = super().__new__(cls, name, bases, attrs)
        init = getattr(new_type, "__init__") # type: _Callable[..., None]
        # NOTE: local `init` is always defined, becuase of `Engine.__init__` + sorted bases
        @_wraps(init)
        def _init_wrapper(self: Engine, *args, **kwargs) -> None:
            init(self, *args, **kwargs)
            self.setup() # calls method after __init__
        setattr(new_type, "__init__", _init_wrapper)
        return new_type


class _EngineMeta(_EngineInitWrapperMeta, _EngineMixinSortMeta, type): ...


class Engine(metaclass=_EngineMeta):
    def __new__(cls: type[_EngineType], *args: _Any, **kwargs: _Any) -> _EngineType:
        instance = super().__new__(cls, *args, **kwargs) # type: _EngineType  # type: ignore[reportAssignmentType]
        instance.fps = cls.fps
        instance.clock = cls.clock
        instance.screen = cls.screen
        return instance # type: ignore
    
    fps: float = 16
    clock: _Clock = _DeltaClock(fps)
    screen: _Screen = _Screen()
    is_running: bool = False

    def __init__(self) -> None:
        ...
    
    def with_fps(self, fps: float, /):
        self.fps = fps
        self.clock.tps = fps
        return self
    
    def with_clock(self, clock: _Clock, /):
        self.clock = clock.with_tps(self.fps)
        return self
    
    def with_screen(self, screen: _Screen, /):
        self.screen = screen
        return self
    
    def setup(self) -> None:
        ...
    
    def update(self, delta: float) -> None:
        ...
    
    def run(self) -> None:
        delta = self.clock.get_delta()
        self.is_running = True
        while self.is_running:
            self.update(delta)
            for queued_node in _Node._queued_nodes:
                queued_node.free()
            _Node._queued_nodes *= 0 # faster way to do `.clear()`
            for node in _Node.iter_nodes():
                node.update(delta)
            self.screen.refresh()
            self.clock.tick()
            delta = self.clock.get_delta()
