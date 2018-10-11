from monads.maybe import Just, Nothing, maybe


def test_maybe_none():
    assert isinstance(maybe(None), Nothing)


def test_maybe_something():
    assert isinstance(maybe(False), Just)


def test_maybe_boolean_false():
    assert isinstance(maybe(False, predicate=bool), Nothing)


def test_maybe_boolean_true():
    assert isinstance(maybe(True, predicate=bool), Just)
