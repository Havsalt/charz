from __future__ import annotations

from typing import NoReturn, Any, final

from ._non_negative import NonNegative


class TimeClassProperties(type):
    delta = NonNegative[float](0)


@final
class Time(metaclass=TimeClassProperties):
    """`Time` is a class namespace used to store delta time

    `Time.delta` is computed by `Clock`, handled by `Engine` frame task,
    usually used in `Node.update`
    """

    # Prevent instantiating,
    # as this class only has class methods and class variables
    def __new__(cls, *_args: Any, **_kwargs: Any) -> NoReturn:
        raise RuntimeError(f"{cls.__name__} cannot be instantiated")
