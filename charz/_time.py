from __future__ import annotations

from typing import NoReturn, Any, final

from ._non_negative import NonNegative


@final
class Time:
    """`Time` is a class namespace used to store delta time.

    `Time.delta` is computed by `Clock`, handled by `Engine` frame task.
    `Time.delta` is usually used in `Node.update`,
    for syncing movement with real time seconds.

    Example:

    ```python
    from charz import Sprite, Time

    class GravityBox(Sprite):
        _GRAVITY_STRENGTH: float = 20  # Positive value means falling down
        _speed_y: float = 0
        texture = [
            "####",
            "####",
            "####",
        ]

        def update(self) -> None:
            # m/s^2 * s = m/s
            self._speed_y += self.GRAVITY_STRENGTH * Time.delta
            # m/s * s = m
            self.position.y += self._speed_y * Time.delta
    ```
    """

    delta = NonNegative[float](0)

    def __new__(cls, *_args: Any, **_kwargs: Any) -> NoReturn:
        raise RuntimeError(f"{cls.__name__} cannot be instantiated")
