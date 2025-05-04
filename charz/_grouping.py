from enum import Enum, unique

from charz_core import CoreGroup


# TODO: Use `StrEnum` for Python 3.11+
@unique
class Group(str, Enum):
    # NOTE: variants in this enum produces the same hash as if it was using normal `str`
    NODE = CoreGroup.NODE
    TEXTURE = "texture"
    COLLIDER = "collider"
