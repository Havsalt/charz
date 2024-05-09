from __future__ import annotations as _annotations


def lerp(start: int | float, end: int | float, weight: float, /) -> float:
    """Lerps between `start` and `end` with `weight` ranging from 0 to 1

    Args:
        start (int | float): starting number
        end (int | float): target number
        weight (float): percentage to lerp

    Returns:
        float: result of the interpolation
    """
    return (1.0 - weight) * start + (weight * end)


def sign(number: int | float, /) -> int:
    """Returns the sign of the number. The number 0 will return 0

    Args:
        number (int | float): number to get the sign of

    Returns:
        int: sign
    """
    return 0 if number == 0 else (1 if number > 0 else -1)


def clamp(number: int | float, smallest: int | float, largest: int | float, /) -> int | float:
    """Returns the number clamped between smallest and largest (inclusive)

    Args:
        number (int | float): number to clamp
        smallest (int | float): lower bound
        largest (int | float): upper bound

    Returns:
        int | float: clamped number
    """
    return max(smallest, min(largest, number))
