from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar

from .monad import Monad

T = TypeVar("T")
S = TypeVar("S")
F = Callable[[T], S]


class Reader(Monad[T]):
    def __init__(self, function: F) -> None:
        self.function = function

    def map(self, function: F) -> Reader:
        return Reader(lambda x: function(self.function(x)))
