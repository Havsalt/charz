from __future__ import annotations

from charz_core import Scene

from ._grouping import Group


# Define additional frame tasks


def update_animations(current_scene: Scene) -> None:
    for animated_node in current_scene.get_group_members(Group.ANIMATED):
        animated_node.update_animation()  # type: ignore  # Skip asserts


# Register additional frame tasks
Scene.frame_tasks[70] = update_animations
