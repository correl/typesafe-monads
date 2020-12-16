import pytest  # type: ignore
from typing import Type
from monads import Maybe, List, Result, Set


@pytest.fixture(scope="module", params=[Maybe, List, Result, Set])
def monad(request) -> Type:
    return request.param
