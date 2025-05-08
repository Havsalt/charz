from __future__ import annotations

import charz_core

from ._grouping import Group
from ._components._animated import Animated


class Scene(charz_core.Scene):
    def process(self) -> None:
        super().process()
        for animated_node in charz_core.Scene.current.get_group_members(Group.ANIMATED):
            assert isinstance(
                animated_node, Animated
            ), f"node {animated_node} missing Animated mixin"
            animated_node.update_animation()


# TODO: make this automatic
# set current scene to this spesific default implementation
# - this is done automatically after this point,
#   as long as `charz.Scene` is used,
#   and not `charz_core.Scene` is called `.current` on
Scene.current = Scene()
