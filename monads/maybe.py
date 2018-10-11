from __future__ import annotations
from typing import Any, Callable, Generic, Optional, TypeVar
from .monad import Monad

T = TypeVar("T")
S = TypeVar("S")
E = TypeVar("E")


class Maybe(Monad[T]):
    def __init__(self) -> None:
        raise NotImplementedError

    @classmethod
    def unit(cls, value: T) -> Maybe[T]:
        return Just(value)

    def bind(self, function: Callable[[T], Maybe[S]]) -> Maybe[S]:
        if isinstance(self, Just):
            return function(self.value)
        else:
            new: Maybe[S] = Nothing()
            return new

    def fmap(self, function: Callable[[T], S]) -> Maybe[S]:
        if isinstance(self, Just):
            return Just(function(self.value))
        else:
            new: Maybe[S] = Nothing()
            return new

    def withDefault(self, default: T) -> T:
        if isinstance(self, Just):
            return self.value
        else:
            return default

    __rshift__ = bind
    __mul__ = __rmul__ = fmap


class Just(Maybe[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"<Just {self.value}>"


class Nothing(Maybe[T]):
    def __init__(self) -> None:
        ...

    def __repr__(self) -> str:
        return "<Nothing>"


def maybe(value: T, predicate: Optional[Callable[[T], bool]] = None) -> Maybe[T]:
    predicate = predicate or (lambda x: x is not None)
    if predicate(value):
        return Just(value)
    else:
        return Nothing()
