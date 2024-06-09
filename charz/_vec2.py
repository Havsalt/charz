from __future__ import annotations as _annotations

from dataclasses import dataclass as _dataclass
from math import (
    sqrt as _sqrt,
    cos as _cos,
    sin as _sin,
    atan2 as _atan2,
    inf as _INF
)
from typing import TypeVar as _TypeVar

from .linear_algebra import (
    lerp as _lerp,
    clamp as _clamp,
    sign as _sign
)

_Vec = _TypeVar("_Vec", bound="Vec2")


@_dataclass
class Vec2:
    """`Vector2` data structure

    Components: `x`, `y`

    Usefull for storing position or direction
    """
    __slots__ = ("x", "y")

    @classmethod
    @property
    def ZERO(cls: type[_Vec]) -> _Vec:
        return cls(0, 0)

    @classmethod
    @property
    def ONE(cls: type[_Vec]) -> _Vec:
        return cls(1, 1)
    
    @classmethod
    @property
    def INF(cls: type[_Vec]) -> _Vec:
        return cls(_INF, _INF)
    
    @classmethod
    @property
    def LEFT(cls: type[_Vec]) -> _Vec:
        return cls(-1, 0)
    
    @classmethod
    @property
    def RIGHT(cls: type[_Vec]) -> _Vec:
        return cls(1, 0)
    
    @classmethod
    @property
    def UP(cls: type[_Vec]) -> _Vec:
        return cls(0, 1)

    @classmethod
    @property
    def DOWN(cls: type[_Vec]) -> _Vec:
        return cls(0, -1)

    def __init__(self, x: float = 0, y: float = 0, /) -> None:
        """Initializes the Vec2

        Args:
            x (float, optional): x component. Defaults to 0.
            y (float, optional): y component. Defaults to 0.
        """
        self.x = x
        self.y = y
    
    def __reduce__(self) -> tuple[type, tuple[float, float]]:
        return (self.__class__, (self.x, self.y))

    def __repr__(self) -> str:
        """Representation with class name an memory address

        Returns:
            str: representation of the vector
        """
        return f"<{self.__class__.__name__} object at {hex(id(self))}>"
    
    def __str__(self) -> str:
        """String representation

        Returns:
            str: representation containing the x and y component
        """
        return f"{self.__class__.__name__}({self.x}, {self.y})"
    
    def __bool__(self) -> bool:
        """Returns whether x or y is not zero

        Returns:
            bool: truthiness
        """
        return bool(self.x or self.y)

    def __abs__(self) -> Vec2:
        return Vec2(abs(self.x), abs(self.y))

    def __round__(self, ndigits: int = 0) -> Vec2:
        return Vec2(round(self.x, ndigits),
                    round(self.y, ndigits))

    def __neg__(self) -> Vec2:
        return Vec2(-self.x, -self.y)
    
    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x,
                    self.y + other.y)

    def __iadd__(self, other: Vec2) -> Vec2:
        self.x += other.x
        self.y += other.y
        return self
    
    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x,
                    self.y - other.y)

    def __isub__(self, other: Vec2) -> Vec2:
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x,
                        self.y * other.y)
        return Vec2(self.x * other,
                    self.y * other)
    
    def __imul__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self
    
    def __floordiv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x // other.x,
                        self.y // other.y)
        return Vec2(self.x // other,
                    self.y // other)
    
    def __ifloordiv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            self.x //= other.x
            self.y //= other.y
        else:
            self.x //= other
            self.y //= other
        return self
    
    def __truediv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x,
                        self.y / other.y)
        return Vec2(self.x / other,
                    self.y / other)
    
    def __itruediv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
        return self
    
    def __mod__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x % other.x,
                        self.y % other.y)
        return Vec2(self.x % other,
                    self.y % other)
    
    def __imod__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            self.x %= other.x
            self.y %= other.y
        else:
            self.x %= other
            self.y %= other
        return self
    
    def __copy__(self) -> Vec2:
        return __class__(self.x, self.y)
    
    def __deepcopy__(self, _memo) -> Vec2:
        return __class__(self.x, self.y)

    def to_tuple(self) -> tuple[float, float]:
        """Converts the vector to a tuple representation

        Returns:
            tuple[float, float]: x and y as tuple
        """
        return (self.x, self.y)

    def copy(self) -> Vec2:
        """Returns a copied Vec2

        Returns:
            Vec2: a new copy
        """
        return __class__(self.x, self.y)

    def length(self) -> float:
        """Returns the length of the vector

        Returns:
            float: length
        """
        if self.x == 0 and self.y == 0:
            return 0.0
        return _sqrt(self.x*self.x + self.y*self.y)
    
    def distance_to(self, other: Vec2) -> float:
        """Returns the relative distance to the other point

        Args:
            other (Vec2): other point

        Returns:
            float: distance
        """
        return (other - self).length()
    
    def normalized(self) -> Vec2:
        """Returns a vector with length of 1, still with same direction

        Returns:
            Vec2: normalized vector
        """
        length = self.length()
        if length == 0:
            return Vec2(0, 0)
        return self / self.length()
    
    def dot(self, other: Vec2) -> float:
        """Returns the dot product between two 2D vectors

        Args:
            other (Vec2): other vector

        Returns:
            float: dot product
        """
        return self.x * other.x + self.y * other.y

    def direction_to(self, other: Vec2) -> Vec2:
        """Returns the direction to the other point

        Args:
            other (Vec2): other point

        Returns:
            Vec2: direction
        """
        return (other - self).normalized()

    def angle(self) -> float:
        """Returns the angle (measured in radians), using atan2

        Returns:
            float: angle given in radians
        """
        return _atan2(self.y, self.x)

    def angle_to(self, other: Vec2) -> float:
        """Returns the angle (measured in radians) to the other point

        Args:
            other (Vec2): other point

        Returns:
            float: angle given in radians
        """
        return (other - self).angle()

    def lerp(self, target: Vec2, weight: float, /) -> Vec2:
        """Lerp towards vector `target` with `weight` ranging from 0 to 1

        Args:
            target (Vec2): target to lerp towards
            weight (int | float): percentage to lerp

        Returns:
            Vec2: vector after performing interpolation
        """
        return Vec2(_lerp(self.x, target.x, weight),
                    _lerp(self.y, target.y, weight))

    def sign(self) -> Vec2:
        """Returns a Vec2 with each component being the sign of the vector

        Returns:
            Vec2: vector with signed components
        """
        return Vec2(_sign(self.x), _sign(self.y))

    def clamped(self, smallest: Vec2, largest: Vec2, /) -> Vec2:
        """Returns a new clamped vector

        Args:
            smallest (Vec2): lower bound for x and y
            largest (Vec2): upper bound for x and y

        Returns:
            Vec2: vector clamped
        """
        return Vec2(_clamp(self.x, smallest.x, largest.x), _clamp(self.y, smallest.y, largest.y))
    
    def rotated(self, angle: float, /) -> Vec2:
        """Returns a vector rotated by `angle` given in radians

        Args:
            angle (float): radians to rotate with

        Returns:
            Vec2: rotated vector
        """
        cos_rad = _cos(angle)
        sin_rad = _sin(angle)
        x = cos_rad * self.x + sin_rad * self.y
        y = -sin_rad * self.x + cos_rad * self.y
        return Vec2(x, y)
    
    def rotated_around(self, angle: float, point: Vec2, /) -> Vec2:
        """Returns a vector rotated by `angle` given in radians, around `point`

        Args:
            angle (float): radians to rotate with
            point (Vec2): point to rotate around

        Returns:
            Vec2: vector rotated around `point`
        """
        diff = self - point
        cos_rad = _cos(angle)
        sin_rad = _sin(angle)
        x = point.x + cos_rad * diff.x + sin_rad * diff.y
        y = point.y + -sin_rad * diff.x + cos_rad * diff.y
        return Vec2(x, y)


class Vec2i(Vec2):
    """`Vector2 integer` data structure

    Components: `x`, `y` only type `int`

    Usefull for storing whole numbers in 2D space
    """
    __slots__ = ("x", "y")

    def __init__(self, x: int = 0, y: int = 0, /) -> None:
        """Initializes the Vec2i

        Args:
            x (int, optional): x component. Defaults to 0.
            y (int, optional): y component. Defaults to 0.
        """
        self.x = x
        self.y = y
    
    def __abs__(self) -> Vec2:
        return Vec2(abs(self.x), abs(self.y))
    
    def __neg__(self) -> Vec2i:
        return Vec2i(-self.x, -self.y)

    def __add__(self, other: Vec2i | Vec2) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x + other.x),
                         int(self.y + other.y))
        return Vec2(self.x + other.x,
                    self.y + other.y)
    
    def __iadd__(self, other: Vec2i) -> Vec2i:
        self.x += other.x
        self.y += other.y
        return self
    
    def __sub__(self, other: Vec2i | Vec2) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x - other.x),
                         int(self.y - other.y))
        return Vec2(self.x - other.x,
                    self.y - other.y)
    
    def __isub__(self, other: Vec2i) -> Vec2i:
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __mul__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x * other.x),
                         int(self.y * other.y))
        elif isinstance(other, Vec2):
            return Vec2(self.x * other.x,
                        self.y * other.y)
        return Vec2(self.x * other,
                    self.y * other)
    
    def __imul__(self, other: Vec2i) -> Vec2i:
        self.x *= other.x
        self.y *= other.y
        return self
    
    def __floordiv__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(self.x // other.x,
                         self.y // other.y)
        elif isinstance(other, Vec2):
            return Vec2(self.x // other.x,
                        self.y // other.y)
        elif isinstance(other, int):
            return Vec2i(self.x // other,
                         self.y // other)
        return Vec2(self.x // other,
                    self.y // other)
    
    def __ifloordiv__(self, other: Vec2i) -> Vec2i:
        self.x //= other.x
        self.y //= other.y
        return self
    
    def __truediv__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x / other.x),
                         int(self.y / other.y))
        elif isinstance(other, Vec2):
            return Vec2(self.x / other.x,
                        self.y / other.y)
        return Vec2(self.x / other,
                    self.y / other)
    
    def __itruediv__(self, other: Vec2i) -> Vec2i:
        self.x /= other.x
        self.y /= other.y
        return self
    
    def __mod__(self, other: Vec2i | Vec2 | int | float) -> Vec2i | Vec2:
        if isinstance(other, Vec2i):
            return Vec2i(int(self.x % other.x),
                         int(self.y % other.y))
        elif isinstance(other, Vec2):
            return Vec2(self.x % other.x,
                        self.y % other.y)
        return Vec2(self.x % other,
                    self.y % other)
    
    def __imod__(self, other: Vec2i) -> Vec2i:
        self.x %= other.x
        self.y %= other.y
        return self
    
    def __copy__(self) -> Vec2i:
        return __class__(self.x, self.y)
    
    def __deepcopy__(self) -> Vec2i:
        return __class__(self.x, self.y)
    
    def to_tuple(self) -> tuple[int, int]:
        """Converts the vector to a tuple representation

        Returns:
            tuple[int, int]: x and y as tuple
        """
        return (self.x, self.y)
    
    def copy(self) -> Vec2i:
        """Returns a copied Vec2i

        Returns:
            Vec2i: a new copy
        """
        return __class__(self.x, self.y)
