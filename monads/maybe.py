from __future__ import annotations
from typing import Any, Callable, Generic, List, Optional, TypeVar
from .monad import Monad
from .monoid import Monoid

T = TypeVar("T")
S = TypeVar("S")
E = TypeVar("E")


class Maybe(Monad[T]):
    def __init__(self) -> None:  # pragma: no cover
        raise NotImplementedError

    @classmethod
    def pure(cls, value: T) -> Maybe[T]:
        return Just(value)

    def bind(self, function: Callable[[T], Maybe[S]]) -> Maybe[S]:
        if isinstance(self, Just):
            return function(self.value)
        else:
            new: Maybe[S] = Nothing()
            return new

    def map(self, function: Callable[[T], S]) -> Maybe[S]:
        if isinstance(self, Just):
            return Just(function(self.value))
        else:
            new: Maybe[S] = Nothing()
            return new

    def apply(self, functor: Maybe[Callable[[T], S]]) -> Maybe[S]:
        if isinstance(functor, Just):
            return self.map(functor.value)
        else:
            new: Maybe[S] = Nothing()
            return new

    def withDefault(self, default: T) -> T:
        if isinstance(self, Just):
            return self.value
        else:
            return default

    @classmethod
    def fromResult(cls, m: Result[T, E]) -> Maybe[T]:
        return m.map(Maybe.pure).withDefault(Nothing())

    def toResult(self, error: E) -> Result[T, E]:
        if isinstance(self, Just):
            return Ok(self.value)
        else:
            return Err(error)

    @classmethod
    def fromList(self, xs: List[T]) -> Maybe[T]:
        if xs:
            return Just(xs[0])
        else:
            return Nothing()

    __rshift__ = bind
    __mul__ = __rmul__ = map


class Just(Maybe[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def __eq__(self, other: object):
        return isinstance(other, Just) and self.value == other.value

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Just {self.value}>"


class Nothing(Maybe[T]):
    def __init__(self) -> None:
        ...

    def __eq__(self, other: object):
        return isinstance(other, Nothing)

    def __repr__(self) -> str:  # pragma: no cover
        return "<Nothing>"


def maybe(value: T, predicate: Optional[Callable[[T], bool]] = None) -> Maybe[T]:
    predicate = predicate or (lambda x: x is not None)
    if predicate(value):
        return Just(value)
    else:
        return Nothing()


class First(Monoid[Maybe[T]]):
    @classmethod
    def mzero(cls) -> First:
        return First(Nothing())

    def mappend(self, other: First):
        if isinstance(self.value, Just):
            return self
        else:
            return other

    def __repr__(self) -> str:  # pragma: no cover
        return f"<First {self.value}>"

    __add__ = mappend


def first(xs: List[Maybe[T]]) -> Maybe[T]:
    return First.mconcat(map(lambda x: First(x), xs)).value


class Last(Monoid[Maybe[T]]):
    @classmethod
    def mzero(cls) -> Last:
        return Last(Nothing())

    def mappend(self, other: Last):
        if isinstance(other.value, Just):
            return other
        else:
            return self

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Last {self.value}>"

    __add__ = mappend


def last(xs: List[Maybe[T]]) -> Maybe[T]:
    return Last.mconcat(map(lambda x: Last(x), xs)).value


# Import Result last to avoid a circular import error
from .result import Result, Ok, Err
