from __future__ import annotations
from functools import reduce
from numbers import Number
from typing import Any, Callable, Generic, Iterator, List, Type, TypeVar, Union

T = TypeVar("T")


class Monoid(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    # FIXME: Other type set to Any, as the proper value (Monoid[T]) is
    # reported as incompatible with subclass implementations due to a
    # flaw in mypy: https://github.com/python/mypy/issues/1317
    def mappend(self, other: Any) -> Monoid[T]:
        raise NotImplementedError

    @classmethod
    def mzero(cls) -> Monoid[T]:
        raise NotImplementedError

    @classmethod
    def mconcat(cls, xs: Iterator[Monoid[T]]) -> Monoid[T]:
        return reduce(cls.mappend, xs, cls.mzero())

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Monoid)
            and type(self) == type(other)
            and self.value == other.value
        )

    __add__ = mappend
