from __future__ import annotations
from functools import reduce
from itertools import chain
from monads import functor
from typing import (
    Callable,
    Iterable,
    Iterator,
    List as _List,
    Optional,
    TypeVar,
    Union,
    cast,
)

from .monad import Monad
from .monoid import Monoidal
from .currying import CurriedBinary, uncurry

T = TypeVar("T")
S = TypeVar("S")


class List(Monad[T], Monoidal[list]):
    @classmethod
    def pure(cls, value: T) -> List[T]:
        return List([value])

    def bind(self, function: Callable[[T], List[S]]) -> List[S]:
        return reduce(List.mappend, map(function, self._value), List.mzero())

    def map(self, function: Callable[[T], S]) -> List[S]:
        return List(list(map(function, self._value)))

    def apply(self, functor: List[Callable[[T], S]]) -> List[S]:

        return List(
            list(chain.from_iterable([map(f, self._value) for f in functor._value]))
        )

    @classmethod
    def mzero(cls) -> List[T]:
        return cls(list())

    @classmethod
    def sequence(cls, xs: Iterable[List[T]]) -> List[_List[T]]:
        """Evaluate monadic actions in sequence, collecting results."""

        def mcons(acc: List[_List[T]], x: List[T]) -> List[_List[T]]:
            return acc.bind(lambda acc_: x.map(lambda x_: acc_ + [x_]))

        empty: List[_List[T]] = List.pure([])
        return reduce(mcons, xs, empty)

    def flatten(self) -> List[T]:
        def flat(acc: List[T], element: T) -> List[T]:
            if element and isinstance(element, Iterable):
                for k in element:
                    acc = acc.mappend(List([k]))
            elif element:
                acc = acc.mappend(List([element]))
            return acc

        return List(reduce(flat, self, List.mzero()))  # type: ignore

    def sort(self, key: Optional[str] = None, reverse: bool = False) -> List[T]:
        lst_copy = self._value.copy()
        lst_copy.sort(key=key, reverse=reverse)  # type: ignore
        return List(lst_copy)

    def fold(
        self, func: Union[Callable[[S, T], S], CurriedBinary[S, T, S]], base_val: S
    ) -> S:
        if isinstance(func, CurriedBinary):
            functor = uncurry(cast(CurriedBinary, func))
        else:
            functor = func
        return reduce(functor, self._value, base_val)  # type: ignore

    __and__ = lambda other, self: List.apply(self, other)  # type: ignore

    def mappend(self, other: List[T]) -> List[T]:
        return List(self._value + other._value)

    __add__ = mappend
    __mul__ = __rmul__ = map
    __rshift__ = bind

    def __sizeof__(self) -> int:
        return self._value.__sizeof__()

    def __len__(self) -> int:
        return len(list(self._value))

    def __iter__(self) -> Iterator[T]:
        return iter(self._value)
