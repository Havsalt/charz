from __future__ import annotations

from types import SimpleNamespace
from functools import partial
from pathlib import Path
from copy import deepcopy
from typing import Iterator

from charz_core import Vec2i, Self

from ._components._texture import load_texture
from ._asset_loader import AssetLoader
from . import text
from ._annotations import Char


class Animation:
    """`Animation` dataclass to represent an animation consisting of multiple frames.

    This class allows you to create an animation from a list of frames
    using `Animation.from_frames`,
    which are lists of strings representing each frame's texture.

    It is possible to subclass this dataclass, but its not easy to say
    what more functionality should be added to it.
    """

    __slots__ = ("frames",)

    @classmethod
    def from_frames(
        cls,
        frames: list[list[str]],
        /,
        *,
        reverse: bool = False,
        flip_h: bool = False,
        flip_v: bool = False,
        fill: bool = True,
        fill_char: Char = " ",
        unique: bool = True,
    ) -> Self:
        """Create an `Animation` from a list of frames/textures.

        Args:
            frames (list[list[str]]): List of frames, where each frame is a list of strings.
            reverse (bool, optional): Reverse the order of frames. Defaults to False.
            flip_h (bool, optional): Flip frames horizontally. Defaults to False.
            flip_v (bool, optional): Flip frames vertically. Defaults to False.
            fill (bool, optional): Fill in to make shape of frames rectangular. Defaults to True.
            fill_char (Char, optional): String of length `1` to fill with. Defaults to " ".
            unique (bool, optional): Whether the frames should be unique instances. Defaults to True.

        Returns:
            Self: An instance of `Animation` (or subclass) with the processed frames.
        """  # noqa: E501
        instance = super().__new__(cls)  # Omit calling `__init__`
        # The negated parameters creates unique list instances,
        # so only copy if they are not present and `unique` is true,
        # else it would be copying an extra time for no reason
        if unique and not reverse and not flip_h and not flip_v and not fill:
            generator = deepcopy(frames)
        else:
            generator = frames

        if fill:  # NOTE: This fill logic has to be before flipping
            generator = map(partial(text.fill_lines, fill_char=fill_char), generator)
        if flip_h:
            generator = map(text.flip_lines_h, generator)
        if flip_v:
            generator = map(text.flip_lines_v, generator)
        if reverse:
            generator = reversed(list(generator))
        instance.frames = list(generator)
        return instance

    def __init__(
        self,
        animation_path: Path | str,
        /,
        *,
        reverse: bool = False,
        flip_h: bool = False,
        flip_v: bool = False,
        fill: bool = True,
        fill_char: Char = " ",
    ) -> None:
        """Load an `Animation` given a path to the folder where the animation is stored.

        Args:
            animation_path (Path | str): Path to folder where animation frames are stored as files.
            flip_h (bool, optional): Flip frames horizontally. Defaults to False.
            flip_v (bool, optional): Flip frames vertically. Defaults to False.
            fill (bool, optional): Fill in to make shape of frames rectangular. Defaults to True.
            fill_char (Char, optional): String of length `1` to fill with. Defaults to " ".
        """  # noqa: E501
        frame_directory = (
            Path.cwd()
            .joinpath(AssetLoader.animation_root)
            .joinpath(animation_path)
            .iterdir()
        )
        generator = map(load_texture, frame_directory)
        if fill:  # NOTE: This fill logic has to be before flipping
            generator = map(partial(text.fill_lines, fill_char=fill_char), generator)
        if flip_h:
            generator = map(text.flip_lines_h, generator)
        if flip_v:
            generator = map(text.flip_lines_v, generator)
        if reverse:
            generator = reversed(list(generator))
        self.frames = list(generator)

    def __repr__(self) -> str:
        # Should never be empty, but if the programmer did it,
        # show empty frame count as 'N/A'
        if not self.frames:
            return f"{self.__class__.__name__}(N/A)"
        longest = 0
        shortest = 0
        tallest = 0
        lowest = 0
        # Variables used in loop to count sizes
        local_longest = 0
        local_shortest = 0
        local_tallest = 0
        local_lowest = 0
        for frame in self.frames:
            # Compare all time best against best results per iteration
            # Allow empty frame and frame with empty lines
            if not frame or not any(frame):
                continue
            local_longest = len(max(frame, key=len))
            longest = max(local_longest, longest)
            local_tallest = len(frame)
            tallest = max(local_tallest, tallest)
            local_shortest = len(min(frame, key=len))
            shortest = min(local_shortest, shortest)
            local_lowest = min(local_lowest, shortest)
        return (
            self.__class__.__name__
            + "("
            + f"{len(self.frames)}"
            + ":{}x{}".format(*self.get_smallest_frame_dimensions())
            + "->{}x{}".format(*self.get_largest_frame_dimensions())
            + ")"
        )

    def get_smallest_frame_dimensions(self) -> Vec2i:
        """Get the smallest frame dimensions in the animation.

        Returns:
            Vec2i: A `Vec2i` object containing the width and height of the smallest frame.
        """
        best_shortest = 0
        best_lowest = 0
        for frame in self.frames:
            if not frame or not any(frame):
                continue
            this_iter_shortest = len(min(frame, key=len))
            best_shortest = min(best_shortest, this_iter_shortest)
            this_iter_lowest = len(frame)
            best_lowest = min(best_lowest, this_iter_lowest)
        return Vec2i(best_shortest, best_lowest)

    def get_largest_frame_dimensions(self) -> Vec2i:
        """Get the largest frame dimensions in the animation.

        Returns:
            Vec2i: A `Vec2i` object containing the width and height of the largest frame.
        """
        best_longest = 0
        best_tallest = 0
        for frame in self.frames:
            if not frame or not any(frame):
                continue
            this_iter_longest = len(max(frame, key=len))
            best_longest = max(best_longest, this_iter_longest)
            this_iter_tallest = len(frame)
            best_tallest = max(best_tallest, this_iter_tallest)
        return Vec2i(best_longest, best_tallest)


class AnimationSet(SimpleNamespace):
    """`AnimationSet` dataclass to represent a collection of animations.

    It is subclassed from `SimpleNamespace` to allow dynamic attribute access.
    """

    __dict__: dict[str, Animation]

    def __init__(self, **animations: Animation) -> None:
        super().__init__(**animations)

    def __getattribute__(self, name: str) -> Animation:
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Animation) -> None:
        return super().__setattr__(name, value)

    def __iter__(self) -> Iterator[Animation]:
        return iter(self.__dict__.values())
