from __future__ import annotations

from enum import Enum, unique

import charz_core


# TODO: Use `StrEnum` for Python 3.11+
@unique
class Group(str, Enum):
    # NOTE: Variants in this enum produces the same hash as if it was using normal `str`
    NODE = charz_core.Group.NODE.value
    TEXTURE = "texture"
    ANIMATED = "animated"
    COLLIDER = "collider"
