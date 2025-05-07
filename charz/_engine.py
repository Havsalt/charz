from __future__ import annotations

import charz_core

from ._clock import Clock
from ._screen import Screen
from ._time import Time


class Engine(charz_core.Engine):
    clock: Clock = Clock(fps=16)
    screen: Screen = Screen()

    def process(self) -> None:
        self.update()
        charz_core.Scene.current.process()
        self.screen.refresh()
        self.clock.tick()
        Time.delta = self.clock.delta

    def run(self) -> None:  # extended main loop function
        Time.delta = self.clock.delta
        # handle special ANSI codes to setup
        self.screen.on_startup()
        super().run()
        # run cleanup function to clear output screen
        self.screen.on_cleanup()
