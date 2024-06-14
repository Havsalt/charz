from __future__ import annotations as _annotations

from typing import Generator as _Generator


class Node:
    uid: int
    parent: Node | None = None
    _instances: dict[int, Node] = {}
    _uid_counter = 0

    def __init__(self) -> None:
        self.uid = Node._uid_counter
        Node._uid_counter += 1

    @classmethod
    def iter_nodes(cls) -> _Generator[Node, None, None]:
        yield from Node._instances.values()

    def setup(self) -> None:
        ...
    
    def update(self, delta: float) -> None:
        ...
