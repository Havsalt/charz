from __future__ import annotations as _annotations

from ._clock import DeltaClock as _DeltaClock
from ._screen import Screen as _Screen
from ._node import Node as _Node


class Engine:
    def __init__(self, fps: float = 16) -> None:
        self.fps = fps
        self.clock = _DeltaClock(fps)
        self.screen = _Screen()
        self.setup()
        self.is_running = True
    
    def setup(self) -> None:
        ...
    
    def update(self, delta: float) -> None:
        ...
    
    def run(self) -> None:
        delta = self.clock.get_delta()
        while self.is_running:
            self.update(delta)
            for queued_node in _Node._queued_nodes:
                queued_node.free()
            _Node._queued_nodes *= 0 # faster way to do `.clear()`
            for node in _Node.iter_nodes():
                node.update(delta)
            self.screen.refresh()
            self.clock.tick()
            delta = self.clock.get_delta()
