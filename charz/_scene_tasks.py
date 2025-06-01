from __future__ import annotations

from charz_core import Scene

from ._grouping import Group
from ._annotations import AnimatedNode


# Define additional frame tasks for `Scene`


def progress_animations(current_scene: Scene) -> None:
    """Update animations for all animated nodes in the current scene."""
    for animated_node in current_scene.get_group_members(
        Group.ANIMATED,
        type_hint=AnimatedNode,
    ):
        animated_node.progress_animation()


# Register additional frame tasks for `Scene`
Scene.frame_tasks[70] = progress_animations
