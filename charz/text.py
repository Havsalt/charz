"""
### Text utility module

Utility for flipping characters/lines. Support for rotating characters

Includes:
- ``
"""

from __future__ import annotations as _annotations

from math import (
    pi as _PI,
    tau as _TAU
)


# IDEA: make TextTranslator (as in Transform props),
#       as public export,
#       and wrap methods of 1 default instance with module functions in this file


# predefined horizontal conversions
_h_conversions: dict[str, str] = { # horizontal flip
    "/": "\\",
    "(": ")",
    "[": "]",
    "{": "}",
    ">": "<",
    "´": "`",
    "d": "b",
    "q": "p",
}
# mirroring `_h_conversions`
_h_conversions.update({
    value: key
    for key, value in _h_conversions.items()
})
# unmirrored `_h_conversions` for monodirectional translations
_h_conversions.update({
    "7": "<"
})
# predefined vertical conversions
_v_conversions: dict[str, str] = { # vertical flip
    "/": "\\",
    ".": "'",
    ",": "`",
    "¯": "_",
    "b": "p",
    "q": "d",
    "w": "m",
    "W": "M",
    "v": "^",
    "V": "A"
}
# mirroring `_v_conversions`
_v_conversions.update({
    value: key
    for key, value in _v_conversions.items()
})
# unmirrored `_v_conversions` for monodirectional translations
_v_conversions.update({
    # none for now...
})
# predefined rotational conversions
_r_conversions: dict[str, tuple[str, ...]] = { # rotational
    "|": ("|", "\\", "-", "/"),
    ".": (".", "'"),
    "b": ("b", "p", "q", "d"),
    "9": ("9", "6")
}
# (I marked vars with underscore as they are not for export, and this is a public module)
# creating mirrored {char: variants} pairs, for pairs already defined in `_r_conversions`
# mirror `_r_conversions` (adds variants as their own keys)
for _options in list(_r_conversions.values()):
    for _idx, _value in enumerate(_options):
        if _idx == 0: # does not need to re-add the initial pair
            continue
        assert _value not in _r_conversions, "cannot add existing value: " + repr(_value)
        _before = _options[:_idx]
        _after = _options[_idx:]
        _new_values = (*_after, *_before)
        _r_conversions[_value] = _new_values
# unmirrored `_r_conversions` for spesific lookup translations
_r_conversions.update({
    # none for now...
})


def flip_h(line: str, /) -> str:
    """Flips a single line horizontally. Also works with a single character

    Args:
        line (list[str]): content to ble flipped

    Returns:
        list[str]: flipped line or character
    """
    return "".join(
        _h_conversions.get(char, char)
        for char in line
    )[::-1]


def flip_v(line: str, /) -> str:
    """Flips a single line vertically. Also works with a single character

    Args:
        line (list[str]): content to ble flipped

    Returns:
        list[str]: flipped line or character
    """
    return "".join(
        _v_conversions.get(char, char)
        for char in line
    )


def flip_lines_h(lines: list[str], /) -> list[str]:
    """Flips lines horizontally. Usefull for flipping textures

    Args:
        lines (list[str]): lines of strings or texture

    Returns:
        list[str]: flipped content
    """
    return list(map(
        lambda line: "".join(
            _h_conversions.get(char, char)
            for char in line
        ),
        lines
    ))[::-1]


def flip_lines_v(lines: list[str], /) -> list[str]:
    """Flips lines vertically. Usefull for flipping textures

    Args:
        lines (list[str]): lines of strings or texture

    Returns:
        list[str]: flipped content
    """
    return list(map(
        lambda line: "".join(
            _v_conversions.get(char, char)
            for char in line
        ),
        lines
    ))


def rotate(char: str, angle: float, /) -> str:
    """Returns symbol when rotated by angle counter clockwise

    Args:
        char (str): character to rotate
        angle (float): counter clockwise rotation in radians

    Returns:
        str: rotated character or original character
    """
    if char in _r_conversions:
        sector_count = len(_r_conversions[char])
        sector_rads = _TAU / sector_count
        half_sector_rads = sector_rads / 2
        total_rads = (angle + half_sector_rads) % _TAU
        index = int(total_rads / sector_rads) % sector_count
        return _r_conversions[char][index]
    return char
