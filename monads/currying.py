from functools import reduce, update_wrapper
from typing import Callable, Generic, NewType, TypeVar, overload

from .reader import Reader

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")

Result = TypeVar("Result")


class CurriedUnary(Reader[A, Result]):
    ...


class CurriedBinary(Reader[A, CurriedUnary[B, Result]]):
    @overload
    def __call__(self, environment: A) -> CurriedUnary[B, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B) -> Result:
        ...

    def __call__(self, *args):
        return reduce(lambda f, x: f(x), args, self.function)


class CurriedTernary(Reader[A, CurriedBinary[B, C, Result]]):
    @overload
    def __call__(self, environment: A) -> CurriedBinary[B, C, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B) -> CurriedUnary[C, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B, c: C) -> Result:
        ...

    def __call__(self, *args):
        return reduce(lambda f, x: f(x), args, self.function)


class CurriedQuaternary(Reader[A, CurriedTernary[B, C, D, Result]]):
    @overload
    def __call__(self, environment: A) -> CurriedTernary[B, C, D, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B) -> CurriedBinary[C, D, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B, c: C) -> CurriedUnary[D, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B, c: C, d: D) -> Result:
        ...

    def __call__(self, *args):
        return reduce(lambda f, x: f(x), args, self.function)


class CurriedQuinary(Reader[A, CurriedQuaternary[B, C, D, E, Result]]):
    @overload
    def __call__(self, environment: A) -> CurriedQuaternary[B, C, D, E, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B) -> CurriedTernary[C, D, E, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B, c: C) -> CurriedBinary[D, E, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B, c: C, d: D) -> CurriedUnary[E, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B, c: C, d: D, e: E) -> Result:
        ...

    def __call__(self, *args):
        return reduce(lambda f, x: f(x), args, self.function)


@overload
def curry(f: Callable[[A], Result]) -> CurriedUnary[A, Result]:
    ...


@overload
def curry(f: Callable[[A, B], Result]) -> CurriedBinary[A, B, Result]:
    ...


@overload
def curry(f: Callable[[A, B, C], Result]) -> CurriedTernary[A, B, C, Result]:
    ...


@overload
def curry(f: Callable[[A, B, C, D], Result]) -> CurriedQuaternary[A, B, C, D, Result]:
    ...


@overload
def curry(
    f: Callable[[A, B, C, D, E], Result]
) -> CurriedQuinary[A, B, C, D, E, Result]:
    ...


def curry(f):
    def wrapped(args, remaining):
        if remaining < 1:
            raise ValueError("Function must take one or more positional arguments")
        elif remaining == 1:
            curried = lambda x: f(*(args + [x]))
            return CurriedUnary(update_wrapper(curried, f))
        else:
            curried = lambda x: wrapped(args + [x], remaining - 1)
            if remaining == 2:
                return CurriedBinary(update_wrapper(curried, f))
            elif remaining == 3:
                return CurriedTernary(update_wrapper(curried, f))
            elif remaining == 4:
                return CurriedQuaternary(update_wrapper(curried, f))
            elif remaining == 5:
                return CurriedQuinary(update_wrapper(curried, f))
            else:
                raise ValueError("Cannot curry a function with more than 5 arguments")

    return wrapped([], f.__code__.co_argcount)


@overload
def uncurry(f: CurriedUnary[A, Result]) -> Callable[[A], Result]:
    ...


@overload
def uncurry(f: CurriedBinary[A, B, Result]) -> Callable[[A, B], Result]:
    ...


@overload
def uncurry(f: CurriedTernary[A, B, C, Result]) -> Callable[[A, B, C], Result]:
    ...


@overload
def uncurry(f: CurriedQuaternary[A, B, C, D, Result]) -> Callable[[A, B, C, D], Result]:
    ...


@overload
def uncurry(
    f: CurriedQuinary[A, B, C, D, E, Result]
) -> Callable[[A, B, C, D, E], Result]:
    ...


def uncurry(f):
    def wrapped(*args):
        return reduce(lambda _f, x: _f(x), args, f)

    return update_wrapper(wrapped, f)
