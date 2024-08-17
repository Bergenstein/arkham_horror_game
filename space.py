"""
This module is responsible for methods, attributes and mechanics related to the Locations in the Arkham Horror Game. Location is defined as a 2D point on an X-Y plane. 
"""

from typing import Self
from .custom_errors import NegativeValueError


class Space:
    """
    :cls:`Space` Represents a location on the board of Arkham Horro Game. Each location is defined by :attr:`_name`, :attr:`_position` (2D X-Y plane), and :attr:`_doom_tokens` (the number of doom tokens present on that location)
    """

    _name: str
    _doom_tokens: int
    _position: tuple[float, float]  # 2D plane

    def __new__(
        cls, name: str, position: tuple[float, float], doom_token: int
    ) -> Self:
        """
        :mth:`__new__` constructor responsible for creating a fresh instance of :cls:`Space` and initializing its attributes
        """
        self = super().__new__(cls)
        self._name = name
        self._position = position
        self._doom_tokens = doom_token
        return self

    @property
    def name(self) -> str:
        return self._name

    @property
    def position(self) -> tuple[float, float]:
        return self._position

    @property
    def doom_tokens(self) -> int:
        return self._doom_tokens

    @doom_tokens.setter
    def doom_tokens(self, value: int) -> None:
        if value < 0:
            raise NegativeValueError(
                value
            )  # custom error preventing setting a negative number of tokens on a location
        self._doom_tokens = value

    def __repr__(self) -> str:
        """
        dunder method for pretty printing string representation of the attributes of the space object.
        """
        return f"Space(name={self._name}, position={self._position}, doom_tokens={self._doom_tokens})"
