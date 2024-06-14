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
    @staticmethod
    def _mixin_sort(base: type) -> bool:
        return issubclass(base, Node)

    def __new__(cls, name: str, bases: tuple[type], attrs: dict[str, object]):
        sorted_bases = tuple(sorted(bases, key=cls._mixin_sort))
        # wrap __init__ for calling setup at the end
        new_type = super().__new__(cls, name, sorted_bases, attrs)
        init = getattr(new_type, "__init__") # type: _Callable[..., None]
        # NOTE: init is always defined, becuase of `Node.__init__` + sorted bases
        @_wraps(init)
        def _init_wrapper(self: Node, *args, **kwargs):
            init(self, *args, **kwargs)
            self.setup()
        setattr(new_type, "__init__", _init_wrapper)
        return new_type


class Node(metaclass=NodeMixinSortMeta):
    _node_instances: dict[int, Node] = {}
    _uid_counter = 0

    def __new__(cls, *args: _Any, **kwargs: _Any):
        instance = super().__new__(cls, *args, **kwargs)
        instance.uid = Node._uid_counter
        Node._uid_counter += 1
        return instance

    @classmethod
    def iter_nodes(cls) -> _Generator[Node, None, None]:
        yield from Node._node_instances.values()

    uid: int
    parent: Node | None = None
    
    def __init__(self) -> None:
        ...

    def setup(self) -> None:
        ...
    
    def update(self, delta: float) -> None:
        ...
