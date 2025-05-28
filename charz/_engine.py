from __future__ import annotations

import charz_core

from ._scene import Scene
from ._clock import Clock
from ._screen import Screen
from ._time import Time


class Engine(charz_core.Engine):
    clock: Clock = Clock(fps=16)
    screen: Screen = Screen()

    def run(self) -> None:  # Extended main loop function
        Time.delta = self.clock.delta
        # Handle special ANSI codes to setup
        self.screen.on_startup()
        super().run()
        # Run cleanup function to clear output screen
        self.screen.on_cleanup()


# Define additional frame tasks


def refresh_screen(engine: Engine) -> None:
    engine.screen.refresh()


def tick_clock(engine: Engine) -> None:
    engine.clock.tick()
    Time.delta = engine.clock.delta


# Register additional frame tasks
# Priorities are chosen with enough room to insert many more tasks in between
Engine.frame_tasks[80] = refresh_screen
Engine.frame_tasks[70] = tick_clock
