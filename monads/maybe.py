from __future__ import annotations
import functools
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
)
from . import result
from .monad import Monad
from .monoid import Monoid

T = TypeVar("T")
S = TypeVar("S")
E = TypeVar("E")


class Maybe(Monad[T]):
    def __init__(self) -> None:  # pragma: no cover
        raise NotImplementedError

    @classmethod
    def pure(cls, value: T) -> Maybe[T]:
        return Just(value)

    def bind(self, function: Callable[[T], Maybe[S]]) -> Maybe[S]:
        if isinstance(self, Just):
            return function(self.value)
        else:
            new: Maybe[S] = Nothing()
            return new

    def map(self, function: Callable[[T], S]) -> Maybe[S]:
        if isinstance(self, Just):
            return Just(function(self.value))
        else:
            new: Maybe[S] = Nothing()
            return new

    def apply(self, functor: Maybe[Callable[[T], S]]) -> Maybe[S]:
        if isinstance(functor, Just):
            return self.map(functor.value)
        else:
            new: Maybe[S] = Nothing()
            return new

    @classmethod
    def sequence(cls, xs: Iterable[Maybe[T]]) -> Maybe[List[T]]:
        """Evaluate monadic actions in sequence, collecting results."""

        def mcons(acc: Maybe[List[T]], x: Maybe[T]) -> Maybe[List[T]]:
            return acc.bind(lambda acc_: x.map(lambda x_: acc_ + [x_]))

        empty: Maybe[List[T]] = cls.pure([])
        return functools.reduce(mcons, xs, empty)

    def withDefault(self, default: T) -> T:
        if isinstance(self, Just):
            return self.value
        else:
            return default

    @classmethod
    def fromResult(cls, m: result.Result[T, E]) -> Maybe[T]:
        return m.map(Maybe.pure).withDefault(Nothing())

    def toResult(self, error: E) -> result.Result[T, E]:
        if isinstance(self, Just):
            return result.Ok(self.value)
        else:
            return result.Err(error)

    @classmethod
    def fromList(self, xs: List[T]) -> Maybe[T]:
        if xs:
            return Just(xs[0])
        else:
            return Nothing()

    __rshift__ = bind
    __and__ = lambda other, self: Maybe.apply(self, other)
    __mul__ = __rmul__ = map


class Just(Maybe[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def __eq__(self, other: object):
        return isinstance(other, Just) and self.value == other.value

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Just {self.value}>"


class Nothing(Maybe[T]):
    def __init__(self) -> None:
        ...

    def __eq__(self, other: object):
        return isinstance(other, Nothing)

    def __repr__(self) -> str:  # pragma: no cover
        return "<Nothing>"


M = TypeVar("M", bound=Monad[Maybe])


class MaybeT(Monad[T], Generic[M, T]):
    def __init__(self, value: Monad[Maybe[T]]) -> None:
        raise NotImplementedError


def transformer(outer: Type[M]) -> Type[MaybeT[M, T]]:
    M = TypeVar("M", bound=Monad[Maybe])
    T = TypeVar("T")

    class _MaybeT(MaybeT[M, T]):
        def __init__(self, value: Monad[Maybe[T]]) -> None:
            self.value = value

        @classmethod
        def pure(cls, value: T) -> MaybeT[M, T]:
            return _MaybeT(outer.pure(Maybe.pure(value)))

        def map(self, function: Callable[[T], S]) -> _MaybeT[M, S]:
            return _MaybeT(self.value.map(lambda inner: inner.map(function)))

        def bind(self, function: Callable[[T], _MaybeT[M, S]]) -> _MaybeT[M, S]:
            def bind_inner(inner: Maybe[T]) -> Monad[Maybe[S]]:
                if isinstance(inner, Just):
                    return function(inner.value).value
                else:
                    empty: Maybe[S] = Nothing()
                    return outer.pure(empty)

            return _MaybeT(self.value.bind(bind_inner))

        def __repr__(self):
            return f"<MaybeT {self.value}>"

        if hasattr(outer, "__await__"):

            def __await__(self) -> Maybe[T]:
                if isinstance(self.value, Awaitable):
                    return self.value.__await__()
                else:
                    raise TypeError("Not awaitable")

    return _MaybeT


def transform(outer: Type[M], instance: Monad[Maybe[T]]) -> MaybeT[M, T]:
    Transformer: Type[MaybeT[M, T]] = transformer(outer)
    return Transformer(instance)


def maybe(value: T, predicate: Optional[Callable[[T], bool]] = None) -> Maybe[T]:
    predicate = predicate or (lambda x: x is not None)
    if predicate(value):
        return Just(value)
    else:
        return Nothing()


class First(Monoid[Maybe[T]]):
    @classmethod
    def mzero(cls) -> First:
        return First(Nothing())

    def mappend(self, other: First):
        if isinstance(self.value, Just):
            return self
        else:
            return other

    def __repr__(self) -> str:  # pragma: no cover
        return f"<First {self.value}>"

    __add__ = mappend


def first(xs: List[Maybe[T]]) -> Maybe[T]:
    return First.mconcat(map(lambda x: First(x), xs)).value


class Last(Monoid[Maybe[T]]):
    @classmethod
    def mzero(cls) -> Last:
        return Last(Nothing())

    def mappend(self, other: Last):
        if isinstance(other.value, Just):
            return other
        else:
            return self

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Last {self.value}>"

    __add__ = mappend


def last(xs: List[Maybe[T]]) -> Maybe[T]:
    return Last.mconcat(map(lambda x: Last(x), xs)).value
