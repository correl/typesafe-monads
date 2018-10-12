from __future__ import annotations
from typing import Any, Callable, TypeVar

from .functor import Functor

T = TypeVar("T")
S = TypeVar("S")


class Applicative(Functor[T]):
    @classmethod
    def pure(cls, value: T) -> Applicative[T]:  # pragma: no cover
        raise NotImplementedError

    # FIXME: Functor type set to Any, as the proper value
    # (Functor[Callable[[T], S]]) is reported as incompatible with subclass
    # implementations due to a flaw in mypy:
    # https://github.com/python/mypy/issues/1317
    def apply(self, functor: Any) -> Functor[S]:  # pragma: no cover
        raise NotImplementedError
