from functools import wraps
from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def flip(function: Callable[[A, B], C]) -> Callable[[B, A], C]:
    """Flip the arguments of a 2-argument function."""

    @wraps(function)
    def flipped(b: B, a: A) -> C:
        return function(a, b)

    return flipped
