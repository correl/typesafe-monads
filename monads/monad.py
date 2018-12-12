from __future__ import annotations
import functools
from typing import Any, Callable, Generic, Iterable, List, TypeVar

from .applicative import Applicative
from .functor import Functor

T = TypeVar("T")
S = TypeVar("S")


class Monad(Applicative[T]):
    # FIXME: Callable return type set to Any, as the proper value
    # (Monad[S]) is reported as incompatible with subclass
    # implementations due to a flaw in mypy:
    # https://github.com/python/mypy/issues/1317
    def bind(self, function: Callable[[T], Any]) -> Monad[S]:  # pragma: no cover
        raise NotImplementedError

    @classmethod
    def pure(cls, value: T) -> Monad[T]:  # pragma: no cover
        raise NotImplementedError

    @classmethod
    def sequence(cls, xs: Iterable[Monad[T]]) -> Monad[List[T]]:
        """Evaluate monadic actions in sequence, collecting results."""

        def reducer(acc: Monad[List[T]], x: Monad[T]) -> Monad[List[T]]:
            return acc.bind(lambda acc_: x.map(lambda x_: acc_ + [x_]))

        return functools.reduce(reducer, xs, cls.pure([]))

    __rshift__ = bind
