from __future__ import annotations
from functools import reduce
from numbers import Complex
from decimal import Decimal
from typing import Any, Callable, Generic, Iterator, Type, TypeVar, Union

T = TypeVar("T")


class Monoid(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    # FIXME: Other type set to Any, as the proper value (Monoid[T]) is
    # reported as incompatible with subclass implementations due to a
    # flaw in mypy: https://github.com/python/mypy/issues/1317
    def mappend(self, other: Any) -> Monoid[T]:  # pragma: no cover
        raise NotImplementedError

    @classmethod
    def mzero(cls) -> Monoid[T]:  # pragma: no cover
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


class Monoidal(Monoid[T]):
    def __repr__(self):  # pragma: no cover
        return repr(self.value)


class String(Monoidal[str]):
    @classmethod
    def mzero(cls) -> Monoidal:
        return cls(str())

    def mappend(self, other: String) -> String:
        return String(self.value + other.value)

    __add__ = mappend


class Addition(Monoidal[Union[int, float]]):
    @classmethod
    def mzero(cls) -> Addition:
        return cls(0)

    def mappend(self, other: Addition) -> Addition:
        return Addition(self.value + other.value)

    __add__ = mappend


class Multiplication(Monoidal[Union[int, float]]):
    @classmethod
    def mzero(cls) -> Multiplication:
        return cls(1)

    def mappend(self, other: Multiplication) -> Multiplication:
        return Multiplication(self.value * other.value)

    __add__ = mappend
