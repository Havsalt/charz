from __future__ import annotations

import sys
from enum import unique

import charz_core


# NOTE: Variants of the enum produces the same hash as if it was using normal `str`
if sys.version_info >= (3, 11):
    from enum import StrEnum, auto

    @unique
    class Group(StrEnum):
        """Enum containing node groups used in `charz`."""

        NODE = charz_core.Group.NODE
        TEXTURE = auto()
        ANIMATED = auto()
        COLLIDER = auto()

else:
    from enum import Enum

    @unique
    class Group(str, Enum):
        """Enum containing node groups used in `charz`."""

        NODE = charz_core.Group.NODE.value
        TEXTURE = "texture"
        ANIMATED = "animated"
        COLLIDER = "collider"
