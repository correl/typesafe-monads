import pytest  # type: ignore
from typing import Type
from monads import Maybe, Result, Reader


@pytest.fixture(scope="module", params=[Maybe, Result])
def monad(request) -> Type:
    return request.param
