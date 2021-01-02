from typing import Any, Union
import pytest  # type: ignore
from monads import List
from monads.currying import curry


def test_fold() -> None:
    m_list: List[int] = List([1, 2, 4])
    total: int = m_list.fold(lambda k, h: k + h, 0)
    assert total == 7

    @curry
    def to_be_curried(offset: int, h: int, k: int) -> int:
        return offset + h + k

    curried_total: int = m_list.fold(to_be_curried(1), 0)
    assert curried_total == 10


def test_flatten() -> None:
    m_list: List[Union[int, List[int]]] = List([1, 2, List([3, 4])])
    assert len(m_list.flatten()) == 4


def test_loop() -> None:
    m_list: List[int] = List([1, 2, 4])
    x = 0
    for i in m_list:
        x = x + 1
    assert x == 3


def test_len() -> None:
    m_list: List[int] = List([1, 2, 4])
    assert len(m_list) == 3
    assert m_list
    assert not List.mzero()
