from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar

from .monad import Monad

T = TypeVar("T")
S = TypeVar("S")
E = TypeVar("E")


class Result(Monad[T], Generic[T, E]):
    def __init__(self) -> None:  # pragma: no cover
        raise NotImplementedError

    @classmethod
    def pure(cls, value: T) -> Result[T, E]:
        return Ok(value)

    def bind(self, function: Callable[[T], Result[S, E]]) -> Result[S, E]:
        if isinstance(self, Ok):
            return function(self.value)
        elif isinstance(self, Err):
            new: Result[S, E] = Err(self.err)
            return new
        else:  # pragma: no cover
            raise TypeError

    def map(self, function: Callable[[T], S]) -> Result[S, E]:
        if isinstance(self, Ok):
            return Result.pure(function(self.value))
        elif isinstance(self, Err):
            new: Result[S, E] = Err(self.err)
            return new
        else:  # pragma: no cover
            raise TypeError

    def apply(self, functor: Result[Callable[[T], S], E]) -> Result[S, E]:
        if isinstance(functor, Ok):
            return self.map(functor.value)
        elif isinstance(functor, Err):
            new: Result[S, E] = Err(functor.err)
            return new
        else:  # pragma: no cover
            raise TypeError

    def withDefault(self, default: T) -> T:
        if isinstance(self, Ok):
            return self.value
        else:
            return default

    @classmethod
    def fromMaybe(cls, m: Maybe[T], error: E) -> Result[T, E]:
        return m.map(Result.pure).withDefault(Err(error))

    def toMaybe(self) -> Maybe[T]:
        return self.map(Maybe.pure).withDefault(Nothing())

    __rshift__ = bind
    __mul__ = __rmul__ = map


class Ok(Result[T, E]):
    def __init__(self, value: T) -> None:
        self.value = value

    def __eq__(self, other: object):
        return isinstance(other, Ok) and self.value == other.value

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Ok {self.value}>"


class Err(Result[T, E]):
    def __init__(self, err: E) -> None:
        self.err = err

    def __eq__(self, other: object):
        return isinstance(other, Err) and self.err == other.err

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Err {self.err}>"


def safe(function: Callable[..., T]) -> Callable[..., Result[T, Exception]]:
    """Wraps a function that may raise an exception.

    e.g.:
        @safe
        def bad() -> int:
            raise Exception("oops")

    """

    def wrapped(*args, **kwargs) -> Result[T, Exception]:
        try:
            return Ok(function(*args, **kwargs))
        except Exception as e:
            return Err(e)

    return wrapped


# Import Maybe last to avoid a circular import error
from .maybe import Maybe, Nothing
