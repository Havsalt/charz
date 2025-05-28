from __future__ import annotations

__all__ = ("SimpleMovementComponent",)

from typing import TYPE_CHECKING, NoReturn

from charz_core import TransformComponent, Vec2

from .._time import Time

if TYPE_CHECKING:
    import keyboard
else:
    keyboard = None


def __getattr__(name: str) -> type[SimpleMovementComponent] | NoReturn:
    try:
        global keyboard  # noqa: PLW0603
        if keyboard is None:
            import keyboard as _keyboard

            keyboard = _keyboard
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError(
            "Module 'keyboard' was not found,"
            " use 'charz' with 'keyboard' or 'all' feature flag,"
            " like depending on 'charz[keyboard]' in 'pyproject.toml'"
        ) from error
    if name not in __all__:
        raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")
    return SimpleMovementComponent


class SimpleMovementComponent:  # Component (mixin class)
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

    # TODO: Add automatic wrapping of this function, so no conflict with user `.update`
    def update(self) -> None:
        super().update()  # type: ignore
        assert isinstance(self, TransformComponent), "Missing `TransformComponent`"
        self.position += self.get_movement_direction() * self.speed * Time.delta
