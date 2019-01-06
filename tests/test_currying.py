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
