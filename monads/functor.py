from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
S = TypeVar("S")


class Functor(Generic[T]):
    def map(self, function: Callable[[T], S]) -> Functor[S]:  # pragma: no cover
        raise NotImplementedError

    __mul__ = __rmul__ = map
