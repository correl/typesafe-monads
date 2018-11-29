# Type-safe Monads

[![Build Status](https://travis-ci.com/correl/typesafe-monads.svg?branch=master)](https://travis-ci.com/correl/typesafe-monads)
[![codecov](https://codecov.io/gh/correl/typesafe-monads/branch/master/graph/badge.svg)](https://codecov.io/gh/correl/typesafe-monads)

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

