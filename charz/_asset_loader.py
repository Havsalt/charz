from __future__ import annotations

from pathlib import Path
from typing import Any, NoReturn, final


class AssetLoaderClassProperties(type):
    """Workaround to add class properties to a `AssetLoader`."""

    _texture_root: Path = Path.cwd()
    _animation_root: Path = Path.cwd()

    @property
    def texture_root(cls) -> Path:
        return cls._texture_root

    @texture_root.setter
    def texture_root(cls, new_path: Path | str) -> None:
        cls._texture_root = Path(new_path)
        if not cls._texture_root.exists():
            raise ValueError("Invalid sprite root folder path")

    @property
    def animation_root(cls) -> Path:
        return cls._animation_root

    @animation_root.setter
    def animation_root(cls, new_path: Path | str) -> None:
        cls._animation_root = Path(new_path)
        if not cls.animation_root.exists():
            raise ValueError("Invalid animation root folder path")


@final
class AssetLoader(metaclass=AssetLoaderClassProperties):
    """Configuration namespace for loading assets.

    Paths fields is of type `pathlib.Path`,
    and use setters that allow passing either `pathlib.Path` or `str` paths.

    `NOTE` Variables have to be set **before** importing *local files* in your project.
    It is typical to use `load_texture` or create `Animation` instances
    in the class definition when subclassing `Sprite`/`AnimatedSprite`,
    which means these configuration variables has to be set before being used.

    Example:
    >>> from charz import ..., AssetLoader, ...
    >>> AssetLoader.texture_root = "src/sprites"
    >>> AssetLoader.animation_root = "src/animations"
    >>> from .local_file import ...

    Attributes:
        `texture_root`: `Path` - Relative path to texture/sprites folder.
        `animation_root`: `Path` - Relative path to animations folder.
    """

    def __new__(cls, *_args: Any, **_kwargs: Any) -> NoReturn:
        raise RuntimeError(f"{cls.__name__} cannot be instantiated")
