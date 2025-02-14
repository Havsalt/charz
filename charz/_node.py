from __future__ import annotations

from itertools import count
from typing import (
    Any as _Any,
    ClassVar,
)

from typing_extensions import Self


class NodeMixinSortMeta(type):
    """Node metaclass for initializing `Node` subclass after other `mixin` classes"""

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, object],
    ) -> type:
        def sorter(base: type) -> bool:
            return isinstance(base, Node)

        sorted_bases = tuple(sorted(bases, key=sorter))
        new_type = super().__new__(cls, name, sorted_bases, attrs)
        return new_type


class Node(metaclass=NodeMixinSortMeta):
    _queued_nodes: ClassVar[list[Node]] = []
    _uid_counter: ClassVar[count] = count(0, 1)
    node_instances: ClassVar[dict[int, Node]] = {}

    def __new__(cls, *_args: _Any, **_kwargs: _Any):
        # NOTE: additional args and kwargs are ignored!
        instance = super().__new__(cls)
        instance.uid = next(Node._uid_counter)
        Node.node_instances[instance.uid] = instance
        return instance

    uid: int  # is set in `Node.__new__`
    parent: Node | None = None
    process_priority: int = 0

    def __init__(self, parent: Node | None = None) -> None:
        if parent is not None:
            self.parent = parent

    def with_parent(self, parent: Node | None, /) -> Self:
        self.parent = parent
        return self

    def with_process_priority(self, process_priority: int, /) -> Self:
        self.process_priority = process_priority
        return self

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(#{self.uid})"

    def update(self, delta: float) -> None: ...

    def queue_free(self) -> None:
        if self not in Node._queued_nodes:
            Node._queued_nodes.append(self)

    def _free(self) -> None:
        del Node.node_instances[self.uid]
