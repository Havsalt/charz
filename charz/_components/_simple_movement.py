from __future__ import annotations

__all__ = ("SimpleMovement",)

from typing import TYPE_CHECKING, NoReturn

from linflex import Vec2

from ._transform import Transform

if TYPE_CHECKING:
    import keyboard
else:
    keyboard = None


def __getattr__(name: str) -> type[SimpleMovement] | NoReturn:
    try:
        global keyboard
        if keyboard is None:
            import keyboard as _keyboard

            keyboard = _keyboard
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "module 'keyboard' was not found,"
            " use 'charz' with 'keyboard' or 'all' feature flag,"
            " like depending on 'charz[keyboard]' in 'pyproject.toml'"
        )
    if name not in __all__:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
    return SimpleMovement


class SimpleMovement:  # Component (mixin class)
    speed: float = 16

    def is_moving_left(self) -> bool:
        return keyboard.is_pressed("a")

    def is_moving_right(self) -> bool:
        return keyboard.is_pressed("d")

    def is_moving_up(self) -> bool:
        return keyboard.is_pressed("w")

    def is_moving_down(self) -> bool:
        return keyboard.is_pressed("s")

    def get_movement_direction(self) -> Vec2:
        return Vec2(
            self.is_moving_right() - self.is_moving_left(),
            self.is_moving_down() - self.is_moving_up(),
        )

    def get_movement_direction_strengths(self) -> Vec2:
        return Vec2(
            self.is_moving_right() - self.is_moving_left(),
            self.is_moving_down() - self.is_moving_up(),
        )

    def update(self, delta: float) -> None:
        super().update(delta)  # type: ignore
        assert isinstance(self, Transform), "Missing `Transform` mixin"
        self.position += self.get_movement_direction() * self.speed * delta
