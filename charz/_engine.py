from __future__ import annotations as _annotations

from ._node import Node as _Node
from ._clock import DeltaClock as _DeltaClock
from ._screen import Screen as _Screen


class Engine:
    def __init__(self, fps: float = 16) -> None:
        self.fps = fps
        self.clock = _DeltaClock(fps)
        self.screen = _Screen()
        self.setup()
        self.is_running = True
    
    def setup(self) -> None:
        ...
    
    def run(self) -> None:
        while self.is_running:
            self.screen.clear()
            for node in _Node.iter_nodes():
                self.screen.render(node)






