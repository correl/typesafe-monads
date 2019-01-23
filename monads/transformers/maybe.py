from typing import Any, Awaitable, Callable, Generic, Type, TypeVar

from ..monad import Monad
from ..maybe import Maybe, Just, Nothing, transformer
from .. import future, list

T = TypeVar("T")
S = TypeVar("S")
M = TypeVar("M", bound=Monad[Maybe])
MM = TypeVar("MM", bound=Monad[Monad[Any]])


class MonadTransformer(Monad[T]):
    def __init__(self, value: Monad) -> None:
        """Lift a wrapped Monad into the transformer."""
        self.value = value


class MaybeT(MonadTransformer[T], Generic[M, T]):
    outer: Type[Monad[Maybe[T]]] = Monad

    def __init__(self, value: Monad[Maybe[T]]) -> None:
        """Lift a wrapped Maybe into the transformer."""
        self.value = value

    @classmethod
    def pure(cls, value: T) -> MaybeT[M, T]:
        return MaybeT(cls.outer.pure(Maybe.pure(value)))

    def map(self, function: Callable[[T], S]) -> MaybeT[M, S]:
        return MaybeT(self.value.map(lambda inner: inner.map(function)))

    def bind(self, function: Callable[[T], MaybeT[M, S]]) -> MaybeT[M, S]:
        def bind_inner(inner: Maybe[T]) -> Monad[Maybe[S]]:
            if isinstance(inner, Just):
                return function(inner.value).value
            else:
                empty: Maybe[S] = Nothing()
                return self.outer.pure(empty)

        return MaybeT(self.value.bind(bind_inner))

    def __repr__(self):
        return f"<Maybe {self.outer.__name__} {self.value}>"


class MaybeMaybe(Monad[T]):
    def __init__(self, value: Maybe[Maybe[T]]) -> None:
        self.value = value

    @classmethod
    def pure(cls, value: T) -> MaybeMaybe[T]:
        return MaybeMaybe(Maybe.pure(Maybe.pure(value)))

    def map(self, function: Callable[[T], S]) -> MaybeMaybe[S]:
        return MaybeMaybe(self.value.map(lambda inner: inner.map(function)))

    def bind(self, function: Callable[[T], MaybeMaybe[S]]) -> MaybeMaybe[S]:
        def bind_inner(inner: Maybe[T]) -> Maybe[Maybe[S]]:
            if isinstance(inner, Just):
                return function(inner.value).value
            else:
                empty: Maybe[S] = Nothing()
                return Maybe.pure(empty)

        return MaybeMaybe(self.value.bind(bind_inner))

    def __repr__(self):
        return f"<Maybe Maybe {self.value}>"


class FutureMaybe(MaybeT[future.Future, T]):
    outer = future.Future

    @classmethod
    def pure(cls, value: T) -> MaybeT[future.Future, T]:
        return FutureMaybe(future.Future.pure(Maybe.pure(value)))

    def __await__(self) -> Maybe[T]:
        if isinstance(self.value, Awaitable):
            return self.value.__await__()
        else:
            raise TypeError("Not awaitable")


ListMaybe = transformer(list.List)

reveal_type(MaybeMaybe.pure(5))
reveal_type(MaybeMaybe.pure(5).value)
reveal_type(FutureMaybe.pure(5))
reveal_type(FutureMaybe.pure(5).value)
reveal_type(ListMaybe.pure(5))
