from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
S = TypeVar("S")
E = TypeVar("E")


class Monad(Generic[T]):
    @classmethod
    def unit(cls, value: T) -> Monad[T]:
        raise NotImplementedError

    def bind(self, function: Callable[[T], Any]) -> Monad[S]:
        raise NotImplementedError


class Result(Monad[T], Generic[T, E]):
    def __init__(self) -> None:
        raise NotImplementedError

    @classmethod
    def unit(cls, value: T) -> Result[T, E]:
        return Ok(value)

    def bind(self, function: Callable[[T], Result[S, E]]) -> Result[S, E]:
        if isinstance(self, Ok):
            return function(self.value)
        elif isinstance(self, Err):
            new: Result[S, E] = Err(self.err)
            return new
        else:
            raise TypeError

    def fmap(self, function: Callable[[T], S]) -> Result[S, E]:
        if isinstance(self, Ok):
            return Result.unit(function(self.value))
        elif isinstance(self, Err):
            new: Result[S, E] = Err(self.err)
            return new
        else:
            raise TypeError

    def withDefault(self, default: T) -> T:
        if isinstance(self, Ok):
            return self.value
        else:
            return default

    __rshift__ = bind
    __mul__ = __rmul__ = fmap


class Ok(Result[T, E]):
    def __init__(self, value: T) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"<Ok {self.value}>"


class Err(Result[T, E]):
    def __init__(self, err: E) -> None:
        self.err = err

    def __repr__(self) -> str:
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
