from __future__ import annotations
from functools import reduce
from itertools import chain
from typing import Callable, TypeVar

from .monad import Monad
from .monoid import Monoidal

T = TypeVar("T")
S = TypeVar("S")


class List(Monad[T], Monoidal[list]):
    @classmethod
    def pure(cls, value: T) -> List[T]:
        return List([value])

    def bind(self, function: Callable[[T], List[S]]) -> List[S]:
        return reduce(List.mappend, map(function, self.value), List.mzero())

    def map(self, function: Callable[[T], S]) -> List[S]:
        return List(list(map(function, self.value)))

    def apply(self, functor: List[Callable[[T], S]]) -> List[S]:
        return List(
            list(chain.from_iterable([map(f, self.value) for f in functor.value]))
        )

    @classmethod
    def mzero(cls) -> List[T]:
        return cls(list())

    def mappend(self, other: List[T]) -> List[T]:
        return List(self.value + other.value)

    __add__ = mappend
    __mul__ = __rmul__ = map
    __rshift__ = bind
