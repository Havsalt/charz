from __future__ import annotations as _annotations

from ._clock import DeltaClock as _DeltaClock
from ._screen import Screen as _Screen
from ._node import Node as _Node
from ._texture import Texture as _Texture


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
        delta = 1 / self.fps
        while self.is_running:
            self.update(delta)
            for node in _Node.iter_nodes():
                node.update(delta)
            self.screen.refresh()
            self.clock.tick()
            delta = self.clock.get_delta()






