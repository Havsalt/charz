from __future__ import annotations

import charz_core

from ._clock import Clock
from ._screen import Screen
from ._time import Time


class Engine(charz_core.Engine):
    """Extended `Engine` for managing scenes, clock, and screen.

    It extends the core `Engine` and adds frame tasks
    for managing the clock and screen refresh.

    The run method is wrapped; to set up the screen,
    along side assigning the initial delta time to `Time.delta`.

    Attributes:
        clock (Clock): The clock instance for managing frame timing.
        screen (Screen): The screen instance for rendering output.

    Example:
        >>> from charz import Engine, Screen, Clock
        >>> class MyGame(Engine):
        ...     clock = Clock(fps=8)  # Set frames per second
        ...     screen = Screen(
        ...         width=80,
        ...         height=24,
        ...         initial_clear=True,
        ...     )
        ...     # Could also use a custom `Screen` subclass,
        ...     # implemented in `Rust` for better performance
    """

    clock: Clock = Clock(fps=16)
    screen: Screen = Screen()

    def run(self) -> None:  # Extended main loop function
        """Run app/game, which will start the main loop.

        The loop will run until `is_running` is set to `False.

        This function is also responsible for setting up the `screen`,
        which given as an overridden class attribute of `Engine` subclass.
        """
        Time.delta = self.clock.delta
        # Handle special ANSI codes to setup
        self.screen.on_startup()
        super().run()
        # Run cleanup function to clear output screen
        self.screen.on_cleanup()


# Define additional frame tasks


def refresh_screen(engine: Engine) -> None:
    """Call `refresh` on the screen to update the display."""
    engine.screen.refresh()


def tick_clock(engine: Engine) -> None:
    """Tick the clock to update the delta time."""
    engine.clock.tick()
    Time.delta = engine.clock.delta


# Register additional frame tasks
# Priorities are chosen with enough room to insert many more tasks in between
Engine.frame_tasks[80] = refresh_screen
Engine.frame_tasks[70] = tick_clock
