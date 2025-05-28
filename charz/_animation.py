from __future__ import annotations

from types import SimpleNamespace
from functools import partial
from pathlib import Path
from copy import deepcopy

from charz_core import Self

from ._components._texture import load_texture
from ._asset_loader import AssetLoader
from . import text


class AnimationClassProperties(type):
    """`Animation` class properties

    `NOTE`: Class properties has to be called
    before importing local files in your project:

    >>> from charz import ..., Animation, ...
    >>> Animation.folder_path = "src/animations"
    >>> from .local_file import ...
    """

    _folder_path: Path = Path.cwd()

    @property
    def folder_path(cls) -> Path:
        return cls._folder_path

    @folder_path.setter
    def folder_path(cls, new_path: Path | str) -> None:
        cls._folder_path = Path(new_path)
        if not cls._folder_path.exists():
            raise ValueError("Invalid animation root folder path")


class Animation(metaclass=AnimationClassProperties):
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
        fill_char: str = " ",
        unique: bool = True,
    ) -> Self:
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
        fill_char: str = " ",
    ) -> None:
        """Load an `Animation` given a path to the folder where the animation is stored

        Args:
            folder_path (Path | str): Path to folder where animation frames are stored as files.
            flip_h (bool, optional): Flip frames horizontally. Defaults to False.
            flip_v (bool, optional): Flip frames vertically. Defaults to False.
            fill (bool, optional): Fill in to make shape of frames rectangular. Defaults to True.
            fill_char (str, optional): String of length 1 to fill with. Defaults to " ".
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
            + f":{shortest}x{lowest}"
            + f"->{longest}x{tallest}"
            + ")"
        )


class AnimationSet(SimpleNamespace):
    def __init__(self, **animations: Animation) -> None:
        super().__init__(**animations)

    def __getattribute__(self, name: str) -> Animation:
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Animation) -> None:
        return super().__setattr__(name, value)
