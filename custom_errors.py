"""
Module responsible for setting up a number of exception that are raised in spirit of defensive programming. These exception are used by clients of Arkham Horror game
"""

from typing import TypeVar
from collections.abc import Collection

itemT = TypeVar("itemT")


class CustomError(Exception):
    """
    Base class for exceptions.
    """

    message: str

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NegativeValueError(CustomError):
    """Exception raised when an illegal negative value is provided."""

    value: int

    def __init__(self, value: int) -> None:
        super().__init__(f"{value} cannot be negative")
        self.value = value


class NotFoundError(CustomError):
    """
    Exception raised when an an item isnt found in a collection
    """

    def __init__(self, value: itemT, values: Collection[itemT]) -> None:
        super().__init__(f"{value} was not found in {values}")
        self.value = value
        self.values = values
