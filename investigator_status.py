"""
This module is responsible for the status of the investigator within Arkham Horror Game. It is responsible for setting health, sanity of the investigator and for methods that impact those. It also deals with clues available to investigator. """

from typing import List, Self, Union
from .clue import Clue
from .custom_errors import NegativeValueError


class InvestigatorStatus:
    """
    Class representing the status of an investigator.
    """

    __health: int
    __sanity: int
    _is_defeated: bool

    def __new__(
        cls, health: int, sanity: int, is_defeated: bool = False
    ) -> Self:
        """
        :meth:`__new__` is the constructor that creates and initializes a new instance of InvestigatorStatus class. It initializes :attr:`__health` :attr:`__sanity` :attr:`_is_defeated`.
        Returns:
        Self: The newly created instance of InvestigatorStatus.
        """
        self = super().__new__(cls)
        self.__set_health_sanity(health, sanity)
        self._is_defeated = is_defeated
        return self

    @classmethod
    def _validate_args(cls, health: int, sanity: int) -> tuple[int, int]:
        """
        class method responsible for validating arguments such as health and sanity. This method is used by setters to set :attr:`__health` :attr:`__sanity`.
        """
        if health < 0:
            raise NegativeValueError(health)
        if sanity < 0:
            raise NegativeValueError(sanity)
        return health, sanity

    def __set_health_sanity(self, health: int, sanity: int) -> tuple[int, int]:
        """
        sets :attr:`__health` :attr:`__sanity` of the investigator. Validates arguments first.
        """
        health, sanity = type(self)._validate_args(health, sanity)
        self.__health = health
        self.__sanity = sanity
        return health, sanity

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, val: int) -> None:
        """
        Setter for the :attr:`__health` of the InvestigatorStatus class.
        This setter method updates :attr:`__health` of the :cls:`InvestigatorStatus`. It first calls the private method :meth:`__set_health_sanity` to validate the value. It then assigns the returned health value to the :attr:`__health`.
        """

        self.__health, _ = self.__set_health_sanity(val, self.__sanity)
        self.__health = val

    @property
    def sanity(self) -> int:
        return self.__sanity

    @sanity.setter
    def sanity(self, val: int) -> None:
        """
        Setter for :attr:`__sanity` attribute of the InvestigatorStatus class.
        This setter method updates :attr:`__sanity` of the :cls:`InvestigatorStatus`. It first calls the private method :meth:`__set_health_sanity` to validate the value. It then assigns the returned sanity value to the :attr:`__sanity`.
        """
        _, self.__sanity = self.__set_health_sanity(self.__health, val)
        self.__sanity = val

    @property
    def is_defeated(self) -> bool:
        return self._is_defeated

    def get_status(self) -> Self:
        """
        Returns the current status of the investigator.
        """
        return self

    def take_damage(self, amount: int) -> None:
        """
        Reduces the investigator's health by a specified amount. If amount is negative, raises a NegativeValueError from custom_errors module.
        """

        if self._validate_args(self.__health, self.__sanity):
            if amount < 0:
                raise NegativeValueError(amount)
            self.__health -= amount

    def check_defeat(self) -> bool:
        """checks if an investigator is defeated by checking its health and sanity attributes"""
        return self.__sanity == 0 or self.__health == 0

    def lose_sanity(self, amount: int) -> None:
        """
        Reduces the investigator's sanity by a specified amount. If amount is negative, raises a NegativeValueError from custom_errors module.
        """
        if self._validate_args(self.__health, self.__sanity):
            if amount < 0:
                raise NegativeValueError(amount)
            self.__sanity -= amount

    def heal(self, amount: int) -> None:
        """
        Increases the investigator's health by a given amount to heal by (increase health by). If amount is negative, raises a NegativeValueError from custom_errors module.
        """
        if self._validate_args(self.__health, self.__sanity):
            if amount < 0:
                raise NegativeValueError(amount)
            self.__health += amount

    def restore_sanity(self, amount: int) -> None:
        """
        Increases the investigator's sanity by a given amount.

        """
        if self._validate_args(self.__health, self.__sanity):
            if amount < 0:
                raise NegativeValueError(amount)
            self.__sanity += amount


class InvestigatorClues:
    """
    :cls:`InvestigatorClues`, which represents the list of clues available to an investigator during the game of Arkham Horror. It directly interact with :cls:`Clue`
    """

    __clues: List[Clue]

    def __init__(self, clue: List[Clue]) -> None:
        """
        initializes the clues
        """
        self.__clues = clue

    @property
    def clues(self) -> List[Clue]:
        return self.__clues

    def add_clue(self, clue: Clue) -> None:
        """
        Adds a clue to the investigator's list of clues.
        """
        self.__clues.append(clue)

    def validate_clue(self, clue: Clue) -> bool:
        """
        Check if the given clue is in the list of clues, part of a validation mechanism.
        """
        return clue in self.__clues

    def remove_clue(self, clue: Clue) -> None:
        """
        Removes a specific clue from the investigator's list of clues.
        """
        if clue not in self.__clues:
            raise ValueError(
                "Clue not found in the clues list and hence cannot be removed."
            )
        self.__clues.remove(clue)

    def get_clue(self, description: str) -> Union[Clue, str]:
        """
        Retrieves a clue by its description.

        Returns:
            Union[Clue, str]: The clue with the provided description or a string
            indicating that no such clue was found in the clues list.
        """

        for clue in self.__clues:
            if clue.description == description:
                return clue
        return f"No clue found in {self.__clues} where {description} matches {clue.description}"
