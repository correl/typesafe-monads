import inspect
from monads.currying import curry


def test_curry() -> None:
    def add3(a: int, b: int, c: int) -> int:
        return a + b + c

    assert add3(1, 2, 3) == curry(add3)(1)(2)(3)


def test_call_curried_function_with_multiple_arguments() -> None:
    @curry
    def add5(a: int, b: int, c: int, d: int, e: int) -> int:
        return a + b + c + d + e

    assert add5(1)(2)(3)(4)(5) == add5(1, 2, 3, 4, 5)


def test_curried_function_annotation_matches_original_function() -> None:
    def add3(a: int, b: int, c: int) -> int:
        return a + b + c

    assert inspect.signature(add3) == inspect.signature(curry(add3))


def test_curried_function_annotation_drops_arguments_as_it_is_applied() -> None:
    def add3(a: int, b: int, c: int) -> int:
        return a + b + c

    assert inspect.Signature(
        [
            inspect.Parameter(
                param, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=int
            )
            for param in ["b", "c"]
        ],
        return_annotation=int,
    ) == inspect.signature(curry(add3)(1))
