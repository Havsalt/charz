from __future__ import annotations

from enum import Enum, unique

import charz_core


# TODO: Use `StrEnum` for Python 3.11+
# TODO: Fix right id, and create in `Scene`
@unique
class Group(str, Enum):
    # NOTE: variants in this enum produces the same hash as if it was using normal `str`
    NODE = charz_core.Group.NODE.value
    TEXTURE = "texture"
    COLLIDER = "collider"
