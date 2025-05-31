from __future__ import annotations

from typing import Generic, Any

from ._annotations import Number


class NonNegative(Generic[Number]):
    """`NonNegative` descriptor for attributes that must be non-negative.

    It is generic, with constraints for `int` and `float` types.

    `NOTE` This is only tested on class level attributes, not instance attributes.

    Example:
    >>> class Clock:
    ...     # This ensures that `delta` is always a non-negative float
    ...     # and raises an error if a negative value is assigned
    ...     delta = NonNegative[float](0)

    Raises:
        TypeError: If the value is not `int` or `float`.
        ValueError: If the value is negative.
    """

    def __init__(self, value: Number, /) -> None:
        """Initialize the descriptor with a non-negative value.
        Args:
        value (Number): The initial value, must be non-negative.
        """
        if not isinstance(value, Number.__constraints__):
            raise TypeError(
                f"Attribute '{self._name[1:]}' must be {self._valid_types_message()}"
            )
        if value < 0:
            raise ValueError(f"Attribute '{self._name[1:]}' must be non-negative")
        self.value = value

    def __set_name__(self, _owner: type, name: str) -> None:
        self._name = f"_{name}"

    def __get__(self, instance: Any, _owner: type) -> Number:  # noqa: ANN401
        return getattr(instance, self._name, self.value)

    def __set__(self, instance: Any, value: Number) -> None:  # noqa: ANN401
        if not isinstance(value, Number.__constraints__):
            raise TypeError(
                f"Attribute '{self._name[1:]}' must be {self._valid_types_message()}"
            )
        if value < 0:
            raise ValueError(f"Attribute '{self._name[1:]}' must be non-negative")
        setattr(instance, self._name, value)

    def _valid_types_message(self) -> str:
        return " or ".join(
            f"'{constaint.__name__}'" for constaint in Number.__constraints__
        )
