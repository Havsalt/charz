from __future__ import annotations as _annotations

from copy import deepcopy as _deepcopy
from typing import (
    Callable as _Callable,  # noqa: F401
    Any as _Any,
)

from typing_extensions import Self as _Self

from ._clock import (
    Clock as _Clock,
    DeltaClock as _DeltaClock,
)
from ._screen import Screen as _Screen
from ._node import Node as _Node
from ._annotations import EngineType as _EngineType


class _EngineMixinSortMeta(type):
    """Engine metaclass for initializing `Engine` subclass after other `mixin` classes"""

    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, object]):
        def sorter(base: type) -> bool:
            return isinstance(base, Engine)

        sorted_bases = tuple(sorted(bases, key=sorter))
        new_type = super().__new__(cls, name, sorted_bases, attrs)
        return new_type


class Engine(metaclass=_EngineMixinSortMeta):
    fps: float = 16
    clock: _Clock = _DeltaClock()
    screen: _Screen = _Screen()
    clear_console: bool = False
    hide_cursor: bool = True
    is_running: bool = False

    def __new__(cls: type[_EngineType], *args: _Any, **kwargs: _Any) -> _EngineType:
        instance = super().__new__(cls, *args, **kwargs)  # type: _EngineType  # type: ignore
        # overrides `.clock.tps` with `.fps` set from class attribute
        instance.clock.tps = instance.fps
        return instance  # type: ignore

    def update(self, delta: float) -> None: ...

    def run(self) -> _Self:
        # check if console/stream should be cleared
        if self.clear_console:
            clear_code = "\x1b[2J\x1b[H"
            self.screen.stream.write(clear_code)
            self.screen.stream.flush()
        # hide cursor
        if self.hide_cursor:
            hide_code = "\x1b[?25l"
            self.screen.stream.write(hide_code)
            self.screen.stream.flush()
        delta = self.clock.get_delta()
        self.is_running = True
        while self.is_running:
            self.update(delta)
            for queued_node in _Node._queued_nodes:
                queued_node.free()
            _Node._queued_nodes *= 0  # NOTE: faster way to do `.clear()`
            # NOTE: 'list' is faster than 'tuple', when copying
            for node in list(_Node.node_instances.values()):  # iterating copy
                node.update(delta)
            self.screen.refresh()
            self.clock.tick()
            delta = self.clock.get_delta()
        # show cursor if hidden
        if self.hide_cursor:
            hide_code = "\x1b[?25h"
            self.screen.stream.write(hide_code)
            self.screen.stream.flush()

        return self  # this is for convenience if the desire to read the app state arise
