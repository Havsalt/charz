from __future__ import annotations

import time
from typing import Literal


class Clock:
    """`Clock` base class, without delta time"""

    _tps: float | None = None

    @property
    def tps(self) -> float | None:
        return self._tps

    @tps.setter
    def tps(self, value: float | None) -> None:
        self._tps = value

    @property
    def delta(self) -> Literal[0]:
        """Returns the delta time between ticks

        Returns:
            Literal[0]: always returns 0, since `Clock` class does not calculate delta time
        """  # noqa: E501
        return 0

    def tick(self) -> None:
        """Does nothing on its own. Exists for better coupling, when extending the `Clock` class"""  # noqa: E501
        return


class DeltaClock(Clock):
    """`DeltaClock` class, with delta time calculation"""

    def __init__(self) -> None:
        self._delta: float = 0
        self._target_delta: float = 0
        self._last_tick = time.perf_counter()

    @property
    def tps(self) -> float | None:
        return self._tps

    @tps.setter
    def tps(self, value: float | None) -> None:
        self._tps = value
        if value is not None:
            self._target_delta = 1.0 / value

    @property
    def delta(self) -> float:
        return self._delta

    def tick(self) -> None:
        """Sleeps for the remaining time to maintain desired `tps`"""
        current_time = time.perf_counter()
        elapsed_time = current_time - self._last_tick
        sleep_time = self._target_delta - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)
            self._last_tick = time.perf_counter()
        else:
            self._last_tick = current_time
        self._delta = max(0, sleep_time)
