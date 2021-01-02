from __future__ import annotations
from functools import reduce
from itertools import chain
from monads import functor, List
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    Set as _Set,
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


class Set(Monad[T], Monoidal[set]):
    @classmethod
    def pure(cls, value: T) -> Set[T]:
        def unpack(k: T) -> set:
            s: set = set()
            if isinstance(k, Iterable):
                for v in k:
                    s.union(unpack(v))
            else:
                s.add(k)
            return s

        return Set(unpack(value))

    def bind(self, function: Callable[[T], Set[S]]) -> Set[S]:
        return reduce(Set.mappend, map(function, self._value), Set.mzero())

    def map(self, function: Callable[[T], S]) -> Set[S]:
        return Set(set(map(function, self._value)))

    def apply(self, functor: Set[Callable[[T], S]]) -> Set[S]:

        return Set(
            set(chain.from_iterable([map(f, self._value) for f in functor._value]))
        )

    @classmethod
    def mzero(cls) -> Set[T]:
        return cls(set())

    @classmethod
    def sequence(cls, xs: Iterable[Set[T]]) -> Set[_List[T]]:
        """Evaluate monadic actions in sequence, collecting results."""

        def mcons(acc: Set[_Set[T]], x: Set[T]) -> Set[_Set[T]]:
            return acc.bind(lambda acc_: x.map(lambda x_: acc_.union(set([x_]))))

        empty: Set[_Set[T]] = Set.pure(set())
        return Set(set(reduce(mcons, xs, empty)))  # type: ignore

    def flatten(self) -> Set[T]:
        def flat(acc: Set[T], element: T) -> Set[T]:
            if element and isinstance(element, Iterable):
                for k in element:
                    acc = acc.mappend(Set(set([k])))
            elif element:
                acc = acc.mappend(Set(set([element])))
            return acc

        return Set(reduce(flat, self, Set.mzero()))  # type: ignore

    def sort(self, key: Optional[str] = None, reverse: bool = False) -> Set[T]:
        lst_copy = self._value.copy()
        lst_copy.sort(key=key, reverse=reverse)  # type: ignore
        return Set(lst_copy)

    def fold(
        self, func: Union[Callable[[S, T], S], CurriedBinary[S, T, S]], base_val: S
    ) -> S:
        if isinstance(func, CurriedBinary):
            functor = uncurry(cast(CurriedBinary, func))
        else:
            functor = func
        return reduce(functor, self._value, base_val)  # type: ignore

    __and__ = lambda other, self: Set.apply(self, other)  # type: ignore

    def mappend(self, other: Set[T]) -> Set[T]:
        return Set(self._value.union(other._value))

    __add__ = mappend
    __mul__ = __rmul__ = map
    __rshift__ = bind

    def __sizeof__(self) -> int:
        return self._value.__sizeof__()

    def __len__(self) -> int:
        return len(set(self._value))

    def __iter__(self) -> Iterator[T]:
        return iter(self._value)
