from typing import Callable, Generic, TypeVar

T = TypeVar("T")
S = TypeVar("S")
E = TypeVar("E")


class Maybe(Generic[T]):
    def __init__(self) -> None:
        raise NotImplementedError

    @classmethod
    def unit(cls, value: T) -> Maybe[T]:
        return Just(value)

    def bind(self, function: Callable[[T], Maybe[S]]) -> Maybe[S]:
        if isinstance(self, Just):
            return function(self.value)
        else:
            new: Maybe[S] = Nothing()
            return new

    def fmap(self, function: Callable[[T], S]) -> Maybe[S]:
        if isinstance(self, Just):
            return Just(function(self.value))
        else:
            new: Maybe[S] = Nothing()
            return new

    __rshift__ = bind
    __mul__ = __rmul__ = fmap


class Just(Maybe[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"<Just {self.value}>"


class Nothing(Maybe[T]):
    def __init__(self) -> None:
        ...

    def __repr__(self) -> str:
        return "<Nothing>"


class Result(Generic[T, E]):
    def __init__(self) -> None:
        raise NotImplementedError

    @classmethod
    def unit(cls, value: T) -> Result[T, E]:
        return Ok(value)

    def bind(self, function: Callable[[T], Result[S, E]]) -> Result[S, E]:
        if isinstance(self, Ok):
            return function(self.value)
        elif isinstance(self, Err):
            new: Result[S, E] = Err(self.err)
            return new
        else:
            raise TypeError

    def fmap(self, function: Callable[[T], S]) -> Result[S, E]:
        if isinstance(self, Ok):
            return Result.unit(function(self.value))
        elif isinstance(self, Err):
            new: Result[S, E] = Err(self.err)
            return new
        else:
            raise TypeError

    __rshift__ = bind
    __mul__ = __rmul__ = fmap


class Ok(Result[T, E]):
    def __init__(self, value: T) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"<Ok {self.value}>"


class Err(Result[T, E]):
    def __init__(self, err: E) -> None:
        self.err = err

    def __repr__(self) -> str:
        return f"<Err {self.err}>"


def test_value() -> Result[int, str]:
    return Ok(5)


def test_error() -> Result[int, str]:
    return Err("oops")


def test_map() -> Result[str, str]:
    five: Ok[int, str] = Ok(5)
    return five.fmap(str)


def test_map_infix() -> Result[str, str]:
    five: Ok[int, str] = Ok(5)
    return five * str


def test_bind() -> Result[int, str]:
    five: Ok[int, str] = Ok(5)
    return five.bind(lambda x: Ok(x + 1))


def test_bind_infix() -> Result[int, str]:
    five: Ok[int, str] = Ok(5)
    return five >> (lambda x: Ok(x + 1))


def test_pipeline() -> Result[int, str]:
    class Frobnicator(object):
        @classmethod
        def create(cls, config: dict) -> Result[Frobnicator, str]:
            return Ok(cls())

        def dostuff(self) -> Result[list, str]:
            return Ok(["a", "b", "c", "d"])

    def load_config() -> Result[dict, str]:
        return Ok({"foo": "bar"})

    return (
        load_config()
        >> Frobnicator.create
        >> Frobnicator.dostuff
        >> (lambda res: Ok(len(res)))
    )
