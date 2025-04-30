from __future__ import annotations

from typing import Any

from typing_extensions import Self

from ._clock import Clock, DeltaClock
from ._screen import Screen
from ._scene import Scene


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
    # using setter and getter to prevent subclass def overriding
    _is_running: bool = False

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        # set `.clock.tps` with `.fps` set from class attribute
        instance.clock.tps = instance.fps
        return instance

    @property
    def is_running(self) -> bool:
        return self._is_running

    @is_running.setter
    def is_running(self, run_state: bool) -> None:
        self._is_running = run_state

    def update(self, delta: float) -> None: ...

    def run(self) -> None:  # main loop function
        # handle special ANSI codes to setup
        self.screen.on_startup()

        # activate control property
        self.is_running = True

        while self.is_running:  # main loop
            # update engine
            self.update(self.clock.delta)

            # update nodes in current scene and scene itself
            Scene.current.process(self.clock.delta)

            # render
            self.screen.refresh()

            # sleep remaining time
            self.clock.tick()

        # run cleanup function
        self.screen.on_cleanup()
