from __future__ import annotations as _annotations

from functools import wraps as _wraps
from typing import (
    Any as _Any,
    Generator as _Generator,
    Callable as _Callable
)


class NodeMixinSortMeta(type):
    """Node metaclass for initializing `Node` subclass after other `mixin` classes
    """
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, object]):
        sorter = lambda base: isinstance(base, Node)
        sorted_bases = tuple(sorted(bases, key=sorter))
        new_type = super().__new__(cls, name, sorted_bases, attrs)
        return new_type


class NodeInitWrapperMeta(type):
    """Wraps the `__init__` method with extra logic
    """
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, object]):
        new_type = super().__new__(cls, name, bases, attrs)
        init = getattr(new_type, "__init__") # type: _Callable[..., None]
        # NOTE: local `init` is always defined, becuase of `Node.__init__` + sorted bases
        @_wraps(init)
        def _init_wrapper(self: Node, *args, **kwargs) -> None:
            init(self, *args, **kwargs)
            self.setup() # calls method after __init__
        setattr(new_type, "__init__", _init_wrapper)
        return new_type


class NodeMeta(NodeInitWrapperMeta, NodeMixinSortMeta, type): ...


class Node(metaclass=NodeMeta):
    _node_instances: dict[int, Node] = {}
    _queued_nodes: list[Node] = []
    _uid_counter = 0

    def __new__(cls, *args: _Any, **kwargs: _Any):
        instance = super().__new__(cls, *args, **kwargs)
        instance.uid = Node._uid_counter
        Node._uid_counter += 1
        Node._node_instances[instance.uid] = instance
        return instance

    @classmethod
    def iter_nodes(cls) -> _Generator[Node, None, None]:
        yield from Node._node_instances.values()

    uid: int # is set in `Node.__new__`
    parent: Node | None = None
    process_priority: int = 0
    
    def __init__(self) -> None:
        ...
    
    def with_parent(self, parent: Node | None, /):
        self.parent = parent
        return self
    
    def with_process_priority(self, process_priority: int, /):
        self.process_priority = process_priority
        return self
    
    def __str__(self) -> str:
        return f"{__class__.__name__}(#{self.uid})"

    def setup(self) -> None:
        ...
    
    def update(self, delta: float) -> None:
        ...
    
    def queue_free(self) -> None:
        Node._queued_nodes.append(self)
    
    def free(self) -> None:
        del Node._node_instances[self.uid]
