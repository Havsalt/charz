"""
Text utility module
===================

Utility for flipping characters/lines. Support for rotating characters

Includes
--------

- `fill`
- `flip_h`
- `flip_v`
- `fill_lines`
- `flip_lines_h`
- `flip_lines_v`
- `rotate`
"""

from __future__ import annotations as _annotations

from math import tau as _TAU

from ._annotations import Char


# NOTE: I marked variables with underscores as they are not for export,
#       since this is a publicly exported module of `charz`

# IDEA: Make TextTranslator (as in Transform props),
#       as public export,
#       and wrap methods of 1 default instance with module functions in this file


# Predefined horizontal conversions
_horizontal_conversions: dict[str, str] = {
    "/": "\\",
    "(": ")",
    "[": "]",
    "{": "}",
    ">": "<",
    "´": "`",
    "d": "b",
    "q": "p",
}
# Mirroring `_horizontal_conversions`
# fmt: off
_horizontal_conversions.update({
    value: key
    for key, value in _horizontal_conversions.items()
})
# Unmirrored `_horizontal_conversions` for monodirectional translations
_horizontal_conversions.update({
    "7": "<"
})
# fmt: on
# Predefined vertical conversions
_vertical_conversions: dict[str, str] = {
    "/": "\\",
    ".": "'",
    ",": "`",
    "¯": "_",
    "b": "p",
    "q": "d",
    "w": "m",
    "W": "M",
    "v": "^",
    "V": "A",
}
# Mirroring `_vertical_conversions`
# fmt: off
_vertical_conversions.update({
    value: key
    for key, value in _vertical_conversions.items()
})
# fmt: on
# Unmirrored `_vertical_conversions` for monodirectional translations
# fmt: off
# _vertical_conversions.update({
#     # None for now...
# })
# fmt: on
# Predefined rotational conversions
_rotational_conversions: dict[str, tuple[str, ...]] = {
    "-": ("-", "/", "|", "\\", "-", "/", "|", "\\"),
    ".": (".", "'"),
    "b": ("b", "p", "q", "d"),
    "9": ("9", "6"),
}

# Creating mirrored {char: variants} pairs,
# for pairs already defined in `_rotational_conversions`

# Mirror `_rotational_conversions` (adds variants as their own keys)
for _options in list(_rotational_conversions.values()):
    for _idx, _value in enumerate(_options):
        if _idx == 0:  # Skip existing initial pair
            continue
        if _value in _rotational_conversions:
            # Some char variants occur multiple times
            # NOTE: Define `_rotational_conversions` keys using "resting variants"
            continue
        _before = _options[:_idx]
        _after = _options[_idx:]
        _new_values = (*_after, *_before)
        _rotational_conversions[_value] = _new_values
# Unmirrored `_rotational_conversions` for spesific lookup translations
# fmt: off
# _rotational_conversions.update({
#     # None for now...
# })
# fmt: on


def fill(line: str, *, width: int, fill_char: Char = " ") -> str:
    """Fill a single left-justified line with a string of length `1`.

    Args:
        line (str): Line to be filled.
        width (int): Maximum width of output string.
        fill_char (Char, optional): String of length `1` to fill line. Defaults to " ".

    Returns:
        str: Line filled with fill character.
    """
    return line.ljust(width, fill_char)


def flip_h(line: str, /) -> str:
    """Flip a single line horizontally.

    Also works with a single character.

    Args:
        line (list[str]): Content to be flipped.

    Returns:
        list[str]: Flipped line or character.
    """
    return "".join(_horizontal_conversions.get(char, char) for char in reversed(line))


def flip_v(line: str, /) -> str:
    """Flip a single line vertically.

    Also works with a single character.

    Args:
        line (list[str]): Content to be flipped.

    Returns:
        list[str]: Flipped line or character.
    """
    return "".join(_vertical_conversions.get(char, char) for char in line)


def fill_lines(lines: list[str], *, fill_char: Char = " ") -> list[str]:
    """Fill lines with fill character, based on longest line.

    Usefull for filling textures, so that it gets a nice rectangular shape.
    Good for centering and flipping textures.

    Args:
        lines (list[str]): Lines to be filled.
        fill_char (Char, optional): String of length `1` to fill line. Defaults to " ".

    Returns:
        list[str]: Rectangular filled lines.
    """
    if not lines:  # Allow when there are no lines
        return []  # But still return unique list
    longest = len(max(lines, key=len))
    return [fill(line, width=longest, fill_char=fill_char) for line in lines]


def flip_lines_h(lines: list[str], /) -> list[str]:
    """Flip lines horizontally.

    Usefull for flipping textures.

    Args:
        lines (list[str]): Lines of strings or texture

    Returns:
        list[str]: Flipped content
    """
    return [flip_h(line) for line in lines]


def flip_lines_v(lines: list[str], /) -> list[str]:
    """Flip lines vertically.

    Usefull for flipping textures.

    Args:
        lines (list[str]): Lines of strings or texture.

    Returns:
        list[str]: Flipped content.
    """
    return [flip_v(line) for line in reversed(lines)]


def rotate(char: Char, /, angle: float) -> str:
    """Return symbol when rotated by angle counter clockwise.

    Args:
        char (Char): String of length `1` to rotate.
        angle (float): Counter clockwise rotation in radians.

    Returns:
        str: Rotated character or original character.
    """
    if char in _rotational_conversions:
        sector_count = len(_rotational_conversions[char])
        sector_rads = _TAU / sector_count
        half_sector_rads = sector_rads / 2
        total_rads = (angle + half_sector_rads) % _TAU
        index = int(total_rads / sector_rads) % sector_count
        return _rotational_conversions[char][index]
    return char
