# Type-safe Monads

![Build](https://github.com/correl/typesafe-monads/workflows/Build/badge.svg)
[![codecov](https://codecov.io/gh/correl/typesafe-monads/branch/master/graph/badge.svg)](https://codecov.io/gh/correl/typesafe-monads)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This is an experiment in building monads in Python supported by strict
type annotations. The goal is to be able to compose monads with the
type checker ensuring their correctness.


## Motivation

I'm a fan of monads, but believe they work best with the support of a
strong type system. I've attempted to use libraries like
[PyMonad](https://pypi.org/project/PyMonad/), but been frustrated by a
lack of type constraints preventing incorrect usage. I could've
attempted to add type annotations to one of those libraries, but
building my own is more fun.

This is a fork of the original work by  [Correl Roush](http://correl.phoenixinquis.net/)

I added some utility methods to make it easier to use in my day to day code and better interate with the pythonic style ( ie _List Comprehension_ )

## Installation

There is no *pipy* release  ( yet)

```bash
$ pip install typesafe-monads
```

## Curring

Mixing Higher order functions ( functions that return a function ) with moand is a very common programming style other functional programming languages.
With _curry_ decorator you can transform a function in a _curried_ function: just apss some positional parameters and get back a function with the remaining ones.

```python
@curry
def power(exp: int, base: int ) -> int:
    return math.pow(base, exp)

square_fn = power(2) # a function that returns the square of the parameter

```

## Base Classes

### Functor

#### map (`*`)

Applies a function to the contents of a functor, transforming it from
one thing to another.

The `*` operator implements map on functors, and is both left and
right associative:

```python
def wordcount(s: str):
    return len(s.split())


f.map(wordcount) == wordcount * f == f * wordcount
```

### Applicative

*Extends `Functor`.*

#### pure

Wraps a value in an applicative functor.

e.g.:

    Maybe.pure("abc") == Just("abc")
    Result.pure(123) == Ok(123)

#### apply (`&`)

Transforms the value contained in the instance's functor with a
function wrapped in the same type of functor.

The `&` operator implements apply on applicatives, and is
right-associative.

e.g.:

```python
increment = lambda x: x + 1

Just(3).apply(Just(increment)) == Just(increment) & Just(3) == Just(4)
```

This can be very handily combined with map to apply curried functions
to multiple arguments:

```python
subtract = lambda x: lambda y: x - y

subtract * Just(10) & Just(4) == Just(6)
```

### Monad

*Extends `Applicative`.*

#### bind (`>>`)

Passes the value within the monad through an operation returning the
same type of monad, allowing multiple operations to be chained.

The `>>` operator implements bind on monads, and is left-associative.

```python
@curry
def lookup(key: str, dictionary: Dict[str, str]) -> Maybe[str]:
    try:
        return Just(dictionary[key])
    except KeyError:
        return Nothing()


result = Just({"hello": "world"}).bind(lookup("hello")).bind(lambda s: s.upper())
result = (
    Just({"hello": "world"})
    >> lookup("hello")
    >> (lambda s: s.upper())
)
```

### Monoid

#### mappend (`+`)

Describes an associative binary operation for a type.

#### mzero

Provides an identity value for the `mappend` operation.

#### mconcat

Accumulates a list of values using `mappend`. Returns the `mzero`
value if the list is empty.

## Monads

Wrapped values should be immutable: they are _protected_ from accidental direct writing with *Final* type and the pythonic naming convention.


### Maybe[T]

Represents optional data. A `Maybe` instance of a certain type `T` will
either be a `Just` object wrapping a value of that type, or `Nothing`.

- Mapping a function over `Nothing` will return `Nothing` without
  calling the function.
- Binding an operation with a `Nothing` will return `Nothing` without
  attempting the operation.

### Result[T, E]

Represents a state of success or failure, declaring a type for each. A
`Result` instance will either be an `Ok` object wrapping a value of
the success type `T`, or an `Err` object wrapping a value of the
failure type `E`.

- Mapping a function over an `Err` will return the `Err` unchanged
  without calling the function.
- Binding an operation with an `Err` will return the `Err` unchanged
  without attempting the operation.

### List[T]

Represents a ordered sequence of items.

- Also implements `Monoid`.

### Set[T]

Represents a unordered sequence of unique items.

- Also implements `Monoid`.

### Future[T]

Represents an asynchronous action.

- Also implements `Awaitable`.

### Reader[T]

Represents the application of a function to it's argument.

## Monads as iterable

It is handy to iterate over some monad contents. *List* is obliviously the first candidate:
```python

m_list: List[int] = List([1, 2, 4, 9])
for i in m_list:
    ...

#Or filter with a generator

evens: List[int] = [k for k in m_list if k % 2 == 0 ]

```

If you want to something to happen just if a *Maybe* monad is defined
```python

for n in Just("one"):
  ...

```

The same apply for *Results*

