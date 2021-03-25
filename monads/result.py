from __future__ import annotations
import functools
from typing import Any, Callable, Generic, Iterable, List, Optional, TypeVar

from . import maybe
from .monad import Monad
from .tools import flip

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

    def mapError(self, function: Callable[[E], S]) -> Result[T, S]:
        if isinstance(self, Err):
            return Err(function(self.err))
        elif isinstance(self, Ok):
            return Ok(self.value)
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

    @classmethod
    def sequence(cls, xs: Iterable[Result[T, E]]) -> Result[List[T], E]:
        """Evaluate monadic actions in sequence, collecting results."""

        def mcons(acc: Result[List[T], E], x: Result[T, E]) -> Result[List[T], E]:
            return acc.bind(lambda acc_: x.map(lambda x_: acc_ + [x_]))

        empty: Result[List[T], E] = Result.pure([])
        return functools.reduce(mcons, xs, empty)

    def withDefault(self, default: T) -> T:
        if isinstance(self, Ok):
            return self.value
        else:
            return default

    @classmethod
    def fromMaybe(cls, m: maybe.Maybe[T], error: E) -> Result[T, E]:
        return m.map(Result.pure).withDefault(Err(error))

    def toMaybe(self) -> maybe.Maybe[T]:
        return self.map(maybe.Maybe.pure).withDefault(maybe.Nothing())

    @classmethod
    def fromOptional(cls, value: Optional[T], error: E) -> Result[T, E]:
        if value is None:
            return Err(error)
        else:
            return Ok(value)

    def toOptional(self) -> Optional[T]:
        if isinstance(self, Ok):
            return self.value
        else:
            return None

    __rshift__ = bind

    def and(self: Result[Callable[[T], S], E], other: Result[T, E]) -> Result[S, E]:
        if isinstance(self, Ok) and not callable(self.value):
            return other.rand(self)
        return other.apply(self)

    def rand(self, functor: Result[Callable[[T], S], E]) -> Result[S, E]:
        return self.apply(functor)

    def __and__(self: Result[Callable[[T], S], E], other: Result[T, E]) -> Result[S, E]:
        if isinstance(self, Ok) and not callable(self.value):
            return NotImplemented
        return other.apply(self)

    def __rand__(self, functor: Result[Callable[[T], S], E]) -> Result[S, E]:
        return self.apply(functor)

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
