from __future__ import annotations

from typing import Any

from typing_extensions import Self

from ._clock import Clock, DeltaClock
from ._screen import Screen
from ._node import Node


class EngineMixinSorter(type):
    """Engine metaclass for initializing `Engine` subclass after other `mixin` classes"""

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, object],
    ) -> type:
        def sorter(base: type) -> bool:
            return isinstance(base, Engine)

        sorted_bases = tuple(sorted(bases, key=sorter))
        new_type = super().__new__(cls, name, sorted_bases, attrs)
        return new_type


class Engine(metaclass=EngineMixinSorter):
    fps: float | None = 16
    clock: Clock = DeltaClock()
    screen: Screen = Screen()
    is_running: bool = False

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        # set `.clock.tps` with `.fps` set from class attribute
        instance.clock.tps = instance.fps
        return instance  # type: ignore

    def update(self, delta: float) -> None: ...

    def run(self) -> None:
        delta = self.clock.delta  # initial delta
        self.is_running = True

        while self.is_running:  # main loop
            self.update(delta)
            for queued_node in Node._queued_nodes:
                queued_node._free()
            Node._queued_nodes *= 0  # NOTE: faster way to do `.clear()`
            # NOTE: `list` is faster than `tuple`, when copying
            for node in list(Node.node_instances.values()):  # iterating copy
                node.update(delta)
            self.screen.refresh()
            self.clock.tick()
            delta = self.clock.delta
