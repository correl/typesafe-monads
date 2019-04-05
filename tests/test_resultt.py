from __future__ import annotations

import pytest  # type: ignore

from monads import resultt
from monads.future import Future
from monads.result import Result, Ok, Err


@pytest.mark.asyncio
async def test_bind_ok_future() -> None:
    def get_thing() -> resultt.Future[int, Exception]:
        return resultt.Future.pure(3)

    def do_thing(thing: int) -> resultt.Future[int, Exception]:
        return resultt.Future.pure(thing + 3)

    expected: Result[int, Exception] = Ok(6)
    assert expected == await (get_thing() >> do_thing)


@pytest.mark.asyncio
async def test_bind_ok_async() -> None:
    async def get_thing() -> Result[int, Exception]:
        return Result.pure(3)

    async def do_thing(thing: int) -> Result[int, Exception]:
        return Result.pure(thing + 3)

    expected: Result[int, Exception] = Ok(6)
    assert expected == await resultt.Future(get_thing()).bind(
        lambda thing: resultt.Future(do_thing(thing))
    )
