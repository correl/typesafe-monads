from setuptools import setup  # type: ignore

setup(
    name="Typesafe Monads",
    version="0.1dev",
    packages=["monads"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "mypy", "pytest-mypy"],
)
