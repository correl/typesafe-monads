from __future__ import annotations
from functools import reduce, update_wrapper
from typing import Any, Callable, Generic, Iterable, List, TypeVar

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

    @classmethod
    def sequence(cls, xs: Iterable[Reader[Env, T]]) -> Reader[Env, List[T]]:
        """Evaluate monadic actions in sequence, collecting results."""

        def mcons(acc: Reader[Env, List[T]], x: Reader[Env, T]) -> Reader[Env, List[T]]:
            return acc.bind(lambda acc_: x.map(lambda x_: acc_ + [x_]))

        empty: Reader[Env, List[T]] = cls.pure([])
        return reduce(mcons, xs, empty)

    def __eq__(self, other: object):  # pragma: no cover
        return isinstance(other, Reader) and self.function == other.function

    def __repr__(self):  # pragma: no cover
        module = self.function.__module__
        name = self.function.__name__
        return f"<Reader {module}.{name}>"

    __mul__ = __rmul__ = map
    __rshift__ = bind
    __and__ = lambda other, self: Reader.apply(self, other)
