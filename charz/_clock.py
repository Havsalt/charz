from __future__ import annotations as _annotations

import time as _time


class Clock:
    """`Clock` base class, without delta time"""

    def __init__(self, tps: float, /) -> None:
        """Initializes the clock with a given tps

        Args:
            tps (float): ticks per second
        """
        self.tps = tps
        self._delta_time = 1.0 / tps  # average delta time

    def with_tps(self, tps: float):
        self.tps = tps
        return self

    @property
    def tps(self) -> float:
        return self._tps

    @tps.setter
    def tps(self, value: float) -> None:
        self._tps = value

    def get_delta(self) -> float:
        """Gets the time it took until tick was called again

        Returns:
            float: delta time until last fram
        """
        return self._delta_time

    def tick(self) -> None:
        """Does nothing. Exists for better coupling, when extending the `Clock` class"""
        return


class DeltaClock(Clock):
    """`DeltaClock` calculating `delta time` and sleeps for maintaining desirerd `tps`"""

    def __init__(self, tps: float, /) -> None:
        """Initializes the delta clock with a given tps

        Args:
            tps (float): ticks per second
        """
        self.tps = tps  # calls property setter
        self._delta_time = 1.0 / tps  # initial delta time (optimal scenario)
        self._last_tick = _time.perf_counter()

    @property
    def tps(self) -> float:
        return self._tps

    @tps.setter
    def tps(self, value: float) -> None:
        self._tps = value
        self._target_delta = 1.0 / self._tps

    def tick(self) -> None:
        """Pauses the clock temporay to achieve the desired framerate (tps)"""
        current_time = _time.perf_counter()
        elapsed_time = current_time - self._last_tick
        sleep_time = self._target_delta - elapsed_time
        if sleep_time > 0:
            _time.sleep(sleep_time)
            self._last_tick = _time.perf_counter()
        else:
            self._last_tick = current_time
        self._delta_time = max(0, sleep_time)
