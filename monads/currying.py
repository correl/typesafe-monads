from functools import reduce, update_wrapper
import inspect
from typing import Callable, Generic, NewType, TypeVar, overload

from .reader import Reader

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")

Result = TypeVar("Result")


class Curried(Reader[A, Result]):
    def __repr__(self):  # pragma: no cover
        module = self.function.__module__
        name = getattr(self.function, "__name__", repr(self.function))
        signature = inspect.signature(self)
        return f"<Curried {module}.{name}{signature}>"


class CurriedUnary(Curried[A, Result]):
    ...


class CurriedBinary(Curried[A, CurriedUnary[B, Result]]):
    @overload
    def __call__(self, environment: A) -> CurriedUnary[B, Result]:
        ...

    @overload
    def __call__(self, environment: A, b: B) -> Result:
        ...

    def __call__(self, *args):
        return reduce(lambda f, x: f(x), args, self.function)


class CurriedTernary(Curried[A, CurriedBinary[B, C, Result]]):
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


class CurriedQuaternary(Curried[A, CurriedTernary[B, C, D, Result]]):
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


class CurriedQuinary(Curried[A, CurriedQuaternary[B, C, D, E, Result]]):
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
    signature = inspect.signature(f)
    parameters = list(signature.parameters.values())

    def wrapped(args, remaining):
        if remaining < 1:
            raise ValueError("Function must take one or more positional arguments")
        elif remaining == 1:
            curried = update_wrapper(lambda x: f(*(args + [x])), f)
            curried.__signature__ = signature.replace(
                parameters=parameters[-remaining:]
            )
            return CurriedUnary(curried)
        else:
            curried = update_wrapper(lambda x: wrapped(args + [x], remaining - 1), f)
            curried.__signature__ = signature.replace(
                parameters=parameters[-remaining:]
            )
            if remaining == 2:
                return CurriedBinary(curried)
            elif remaining == 3:
                return CurriedTernary(curried)
            elif remaining == 4:
                return CurriedQuaternary(curried)
            elif remaining == 5:
                return CurriedQuinary(curried)
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
