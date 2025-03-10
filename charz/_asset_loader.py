from __future__ import annotations

from pathlib import Path
from typing import Any, NoReturn, final


class AssetLoaderClassProperties(type):
    # class variables for configuartion
    _texture_root: Path = Path.cwd()
    _animation_root: Path = Path.cwd()

    # NOTE: Theese have to be set before importing local files in your project:
    # from charz importing ..., AssetLoader, ...
    # AssetLoader.texture_root = "src/sprites"
    # AssetLoader.animation_root = "src/animations"
    # from .local_file importing ...

    @property
    def texture_root(cls) -> Path:
        return cls._texture_root

    @texture_root.setter
    def texture_root(cls, new_path: Path | str) -> None:
        cls._texture_root = Path(new_path)
        if not cls._texture_root.exists():
            raise ValueError("invalid sprite root folder path")

    @property
    def animation_root(cls) -> Path:
        return cls._animation_root

    @animation_root.setter
    def animation_root(cls, new_path: Path | str) -> None:
        cls._animation_root = Path(new_path)
        if not cls.animation_root.exists():
            raise ValueError("invalid animation root folder path")


@final
class AssetLoader(metaclass=AssetLoaderClassProperties):
    # prevent instantiating, as this class only has class methods and class variables
    def __new__(cls, *_args: Any, **_kwargs: Any) -> NoReturn:
        raise TypeError(f"{cls.__name__} cannot be instantiated")
