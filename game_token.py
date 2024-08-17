"""
This module provides a basic implementation for tokens used in the Arkham Horror game
"""

from typing import Generic, TypeVar

itemT = TypeVar("itemT")


class Token(Generic[itemT]):
    """
    a generic class :cls:`Token` that can work with any data type itemT
    """

    _token_type: itemT

    def __init__(self, token_type: itemT):
        """
        Initializes a new instance of :cls:`Token` with a specified token of any type: itemT.
        """
        self._token_type = token_type
