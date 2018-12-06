from __future__ import annotations
from functools import reduce, update_wrapper
from typing import Any, Callable, Generic, TypeVar

from .monad import Monad

T = TypeVar("T")
S = TypeVar("S")
Env = TypeVar("Env")
F = Callable[[Env], T]


class Reader(Monad[T], Generic[Env, T]):
    def __init__(self, function: F) -> None:
        update_wrapper(self, function)
        self.function = function

    def __call__(self, environment: Env) -> T:
        return self.function(environment)

    @classmethod
    def pure(cls, value: T) -> Reader[Env, T]:
        f: F = lambda x: value
        return cls(f)

    def map(self, function: Callable[[T], S]) -> Reader[Env, S]:
        f: Callable[[Env], S] = lambda x: function(self.function(x))
        return Reader(f)

    def apply(self, r: Reader[Env, Callable[[T], S]]) -> Reader[Env, S]:
        f: Callable[[Env], S] = lambda x: r.function(x)(self(x))
        return Reader(f)

    def bind(self, function: Callable[[T], Reader[Env, S]]) -> Reader[Env, S]:
        f: Callable[[Env], S] = lambda x: function(self.function(x))(x)
        return Reader(f)

    def __eq__(self, other: object):  # pragma: no cover
        return isinstance(other, Reader) and self.function == other.function

    def __repr__(self):  # pragma: no cover
        module = self.function.__module__
        name = self.function.__name__
        return f"<Reader {module}.{name}>"

    __mul__ = __rmul__ = map
    __rshift__ = bind


class Curried(Reader[Env, T]):
    def __call__(self, *args):
        return reduce(lambda f, x: f(x), args, self.function)


def curry(f: Callable):
    def wrapped(args, remaining):
        if remaining == 0:
            return f(*args)
        else:
            curried = lambda x: wrapped(args + [x], remaining - 1)
            return Curried(update_wrapper(curried, f))

    return wrapped([], f.__code__.co_argcount)
