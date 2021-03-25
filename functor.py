from __future__ import annotations
from typing import Any, Callable, Protocol, TypeVar

T = TypeVar("T")
S = TypeVar("S")

class Functor(Protocol[T, S]):
    def __fmap__(self, function: Callable[[T], S]) -> Functor[S]:
        ...
