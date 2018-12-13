import pytest  # type: ignore
from typing import Type
from monads import Maybe, List, Result, Future


@pytest.fixture(scope="module", params=[Maybe, List, Result])
def monad(request) -> Type:
    return request.param
