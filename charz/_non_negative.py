from __future__ import annotations

from typing import Generic, Any

from ._annotations import Number


class NonNegative(Generic[Number]):
    def __init__(self, value: Number, /) -> None:
        if not isinstance(value, Number.__constraints__):
            raise TypeError(
                f"attribute '{self._name[1:]}' must be {self._valid_types_message()}"
            )
        if value < 0:
            raise ValueError(f"attribute '{self._name[1:]}' must be non-negative")
        self.value = value

    def __set_name__(self, _owner: type, name: str) -> None:
        self._name = f"_{name}"

    def __get__(self, instance: Any, _owner: type) -> Number:  # noqa: ANN401
        return getattr(instance, self._name, self.value)

    def __set__(self, instance: Any, value: Number) -> None:  # noqa: ANN401
        if not isinstance(value, Number.__constraints__):
            raise TypeError(
                f"attribute '{self._name[1:]}' must be {self._valid_types_message()}"
            )
        if value < 0:
            raise ValueError(f"attribute '{self._name[1:]}' must be non-negative")
        setattr(instance, self._name, value)

    def _valid_types_message(self) -> str:
        return " or ".join(
            f"'{constaint.__name__}'" for constaint in Number.__constraints__
        )
