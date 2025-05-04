from __future__ import annotations

import charz_core

from ._screen import Screen


class Engine(charz_core.Engine):
    fps: float | None = 16
    clock = charz_core.DeltaClock()
    screen: Screen = Screen()

    def run(self) -> None:  # main loop function
        # handle special ANSI codes to setup
        self.screen.on_startup()

        # activate control property
        self.is_running = True

        while self.is_running:  # main loop
            # update engine
            self.update(self.clock.delta)

            # update nodes in current scene and scene itself
            charz_core.Scene.current.process(self.clock.delta)

            # render
            self.screen.refresh()

            # sleep remaining time
            self.clock.tick()

        # run cleanup function
        self.screen.on_cleanup()
