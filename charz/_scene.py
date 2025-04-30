from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import Self

from ._grouping import Group
from ._annotations import GroupID

if TYPE_CHECKING:
    from ._engine import Engine
    from ._node import Node


class SceneClassProperties(type):
    _current: Scene

    @property
    def current(cls) -> Scene:
        if not hasattr(cls, "_current"):
            cls._current = Scene()  # Create default scene if none exists
        return cls._current

    @current.setter
    def current(cls, new: Scene) -> None:
        cls.current.on_exit()
        cls._current = new
        new.on_enter()


class Scene(metaclass=SceneClassProperties):
    """`Scene` to encapsulate dimensions/worlds

    When a node is created, it will be handled by the currently active `Scene`.
    If no `Scene` is created, a default `Scene` will be created and set as the active one

    By subclassing `Scene`, and implementing `__init__`, all nodes
    created in that `__init__` will be added to that subclass's group of nodes

    NOTE (Technical): A `Scene` hitting reference count of `0`
    will reduce reference count to its nodes by `1`
    """

    # many of these are set in `Scene.__new__`
    nodes: list[Node]
    groups: dict[GroupID, dict[int, Node]]
    root_ref: Engine | None = None
    _queued_nodes: list[Node]

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        # NOTE: lazyloading `Group`
        # do import here to prevent cycling dependencies,
        # as there won't be a lot of scene creation
        from ._grouping import Group

        # NOTE: when instantiating the scene,
        #       it will be set as the current one
        #     - use preloading to surpass
        Scene._current = instance
        instance.nodes = []
        instance.groups = {group: {} for group in Group}
        instance._queued_nodes = []
        return instance

    @classmethod
    def preload(cls) -> Self:
        previous_scene = Scene.current
        instance = cls()
        Scene.current = previous_scene
        return instance

    def __str__(self) -> str:
        group_counts = ", ".join(f"{group}: {len(self.groups[group])}" for group in Group)
        return f"{self.__class__.__name__}({group_counts})"

    def __init__(self) -> None:  # override in subclass
        ...  # this is where node instantiation goes

    def set_current(self) -> None:
        Scene.current = self

    def as_current(self) -> Self:
        self.set_current()
        return self

    def get_group_members(self, group_id: GroupID, /) -> list[Node]:
        return list(self.groups[group_id].values())

    def get_first_group_member(self, group_id: GroupID, /) -> Node:
        for node in self.groups[group_id].values():
            return node
        raise ValueError()

    def process(self, delta: float) -> None:
        self.update(delta)

        # NOTE: `list` is faster than `tuple`, when copying
        # iterate a copy (hence the use of `list(...)`)
        # to allow node creation during iteration
        for node in list(self.groups[Group.NODE].values()):
            node.update(delta)

        # free queued nodes
        for queued_node in self._queued_nodes:
            queued_node._free()
        self._queued_nodes *= 0  # NOTE: faster way to do `.clear()`

    def on_enter(self) -> None:
        """Triggered when this scene is set as the current one"""

    def on_exit(self) -> None:
        """Triggered when this scene is no longer the current one"""

    def update(self, delta: float) -> None: ...
