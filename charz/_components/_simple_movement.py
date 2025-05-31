from __future__ import annotations

__all__ = ("SimpleMovementComponent",)

from typing import TYPE_CHECKING, NoReturn

from charz_core import TransformComponent, Vec2

from .._time import Time

if TYPE_CHECKING:
    import keyboard
else:
    keyboard = None


# Use lazy loading to allow for not using `keyboard` module, as long as it is never used
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
    """`SimpleMovementComponent` mixin class for node.

    It provides basic movement functionality for a node,
    and allows the node to move in 2D space using the WASD keys.

    Attributes:
        `speed`: `float` - The speed of the node's movement per second (`units/s`).
            Defaults to `16` `units/s`, which is a reasonable speed for most games.
            You can change this value to make the node move faster or slower,
            by overriding this attribute in your node class as a class attribute.

    Methods:
        `is_moving_left`
        `is_moving_right`
        `is_moving_up`
        `is_moving_down`
        `get_movement_direction`
    """

    speed: float = 16

    def is_moving_left(self) -> bool:
        """Check if the node is moving left.

        Override implementation to change the key used for moving left.

        Returns:
            `bool`: `True` if the node is moving left, `False` otherwise.
        """
        return keyboard.is_pressed("a")

    def is_moving_right(self) -> bool:
        """Check if the node is moving right.

        Override implementation to change the key used for moving right.

        Returns:
            `bool`: `True` if the node is moving right, `False` otherwise.
        """
        return keyboard.is_pressed("d")

    def is_moving_up(self) -> bool:
        """Check if the node is moving up.

        Override implementation to change the key used for moving up.

        Returns:
            `bool`: `True` if the node is moving up, `False` otherwise.
        """
        return keyboard.is_pressed("w")

    def is_moving_down(self) -> bool:
        """Check if the node is moving down.

        Override implementation to change the key used for moving down.

        Returns:
            `bool`: `True` if the node is moving down, `False` otherwise.
        """
        return keyboard.is_pressed("s")

    def get_movement_direction(self) -> Vec2:
        """Get the movement direction of the node.

        This method returns a `Vec2` object representing the direction
        of movement based on the current input.

        `NOTE` The returned vector is *not* normalized,
        meaning it can have a length greater than 1.

        Returns:
            `Vec2`: Raw direction vector.
        """
        return Vec2(
            self.is_moving_right() - self.is_moving_left(),
            self.is_moving_down() - self.is_moving_up(),
        )

    # TODO: Add automatic wrapping of this function, so no conflict with user `.update`
    def update(self) -> None:
        """Custom update method for the node.

        Automatically handles checking for movement input,
        and moving the node accordingly.
        """
        super().update()  # type: ignore
        assert isinstance(self, TransformComponent), (
            f"Node {self} missing `TransformComponent`"
        )
        self.position += self.get_movement_direction() * self.speed * Time.delta
