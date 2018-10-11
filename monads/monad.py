from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar

from .functor import Functor

T = TypeVar("T")
S = TypeVar("S")


class Monad(Functor[T]):
    @classmethod
    def unit(cls, value: T) -> Monad[T]:
        raise NotImplementedError

    # FIXME: Callable return type set to Any, as the proper value
    # (Monad[S]) is reported as incompatible with subclass
    # implementations due to a flaw in mypy:
    # https://github.com/python/mypy/issues/1317
    def bind(self, function: Callable[[T], Any]) -> Monad[S]:
        raise NotImplementedError
