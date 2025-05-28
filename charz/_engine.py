from __future__ import annotations

import charz_core

from ._scene import Scene
from ._clock import Clock
from ._screen import Screen
from ._time import Time


class Engine(charz_core.Engine):
    clock: Clock = Clock(fps=16)
    screen: Screen = Screen()

    def process(self) -> None:
        self.update()
        Scene.current.process()
        self.screen.refresh()
        self.clock.tick()
        Time.delta = self.clock.delta

    def run(self) -> None:  # Extended main loop function
        Time.delta = self.clock.delta
        # Handle special ANSI codes to setup
        self.screen.on_startup()
        super().run()
        # Run cleanup function to clear output screen
        self.screen.on_cleanup()
