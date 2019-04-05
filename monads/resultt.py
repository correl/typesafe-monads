from __future__ import annotations
from typing import Any, Awaitable, Callable, Generic, Type, TypeVar

from .monad import Monad
from . import maybe, future, result

T = TypeVar("T")
S = TypeVar("S")
E = TypeVar("E")


class ResultT(Monad[T], Generic[T, E]):
    ...


class Maybe(ResultT[T, E]):
    def __init__(self, value: maybe.Maybe[result.Result[T, E]]) -> None:
        self.value = value

    @classmethod
    def pure(cls, value: T) -> Maybe[T, E]:
        return Maybe(maybe.Maybe.pure(result.Result.pure(value)))

    def map(self, function: Callable[[T], S]) -> Maybe[S, E]:
        return Maybe(self.value.map(lambda inner: inner.map(function)))

    def bind(self, function: Callable[[T], Maybe[S, E]]) -> Maybe[S, E]:
        def bind_inner(inner: result.Result[T, E]) -> maybe.Maybe[result.Result[S, E]]:
            if isinstance(inner, result.Ok):
                return function(inner.value).value
            elif isinstance(inner, result.Err):
                return maybe.Maybe.pure(inner.err)
            else:
                raise TypeError

        return Maybe(self.value.bind(bind_inner))

    def __repr__(self):
        return f"<ResultT<Maybe> {self.value}>"

    __rshift__ = bind
    __and__ = lambda other, self: Maybe.apply(self, other)
    __mul__ = __rmul__ = map


class Result(ResultT[T, E]):
    def __init__(self, value: result.Result[result.Result[T, E], E]) -> None:
        self.value = value

    @classmethod
    def pure(cls, value: T) -> Result[T, E]:
        return Result(result.Result.pure(result.Result.pure(value)))

    def map(self, function: Callable[[T], S]) -> Result[S, E]:
        return Result(self.value.map(lambda inner: inner.map(function)))

    def bind(self, function: Callable[[T], Result[S, E]]) -> Result[S, E]:
        def bind_inner(
            inner: result.Result[T, E]
        ) -> result.Result[result.Result[S, E], E]:
            if isinstance(inner, result.Ok):
                return function(inner.value).value
            elif isinstance(inner, result.Err):
                return result.Result.pure(inner.err)
            else:
                raise TypeError

        return Result(self.value.bind(bind_inner))

    def __repr__(self):
        return f"<ResultT<Result> {self.value}>"

    __rshift__ = bind
    __and__ = lambda other, self: Result.apply(self, other)
    __mul__ = __rmul__ = map


class Future(ResultT[T, E]):
    def __init__(self, value: Awaitable[result.Result[T, E]]) -> None:
        self.value = future.Future(value)

    @classmethod
    def pure(cls, value: T) -> Future[T, E]:
        return Future(future.Future.pure(result.Result.pure(value)))

    def map(self, function: Callable[[T], S]) -> Future[S, E]:
        return Future(self.value.map(lambda inner: inner.map(function)))

    def bind(self, function: Callable[[T], Future[S, E]]) -> Future[S, E]:
        def bind_inner(
            inner: result.Result[T, E]
        ) -> future.Future[result.Result[S, E]]:
            if isinstance(inner, result.Ok):
                return function(inner.value).value
            elif isinstance(inner, result.Err):
                return future.Future.pure(inner.err)
            else:
                raise TypeError

        return Future(self.value.bind(bind_inner))

    def __repr__(self):
        return f"<ResultT<Future> {self.value}>"

    def __await__(self):
        return self.value.__await__()

    __rshift__ = bind
    __and__ = lambda other, self: Future.apply(self, other)
    __mul__ = __rmul__ = map
