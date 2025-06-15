from __future__ import annotations

import time

from ._non_negative import NonNegative


class Clock:
    """`Clock` class, with delta time calculation.

    Used to sleep for the remaining time of the current frame,
    until a new frame should be processed.
    An instance of `Clock` is used by the active `Engine`.
    If you don't want the clock to sleep, set `fps` to `0`.

    Example:
    >>> from charz import Engine, Clock
    >>> class MyGame(Engine):
    ...     clock = Clock(fps=12)

    Attributes:
        `fps`: `NonNegative[float]` - Frames per second. If `0`, it will not sleep.
        `delta`: `property[float]` - Read-only attribute for delta time,
            updated on each `tick` call.
    """

    fps = NonNegative[float](0)

    def __init__(self, *, fps: float = 0) -> None:
        """Initialize with optional `fps`.

        `NOTE` When `fps` is set to `0`, it will **not** do any sleeping,
        which means `delta` will be updated and nothing else happens.

        Args:
            fps (float, optional): Frames per second. Defaults to 0.
        """
        self.fps = fps
        self._delta = 1 / self.fps
        self._last_tick = time.perf_counter()

    def __repr__(self) -> str:
        fps = self.fps  # Assign to temp var to use prettier formatting on next line
        return f"{self.__class__.__name__}({fps=})"

    @property
    def delta(self) -> float:
        """Read-only attribute for delta time.

        Call `tick` to update and mutate properly.
        """
        return self._delta

    def tick(self) -> None:
        """Sleeps for the remaining time to maintain desired `fps`."""
        current_time = time.perf_counter()

        if self.fps == 0:  # Skip sleeping if `.fps` is zero
            self._last_tick = current_time
            return

        target_delta = 1 / self.fps  # Seconds
        elapsed_time = current_time - self._last_tick
        sleep_time = target_delta - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)
            self._last_tick = time.perf_counter()
        else:
            self._last_tick = current_time
        self._delta = max(0, sleep_time)
