"""
Implementation of skills in the Arkham Horror game. It encapsulte the skill test in the Game
"""

from typing import Self, Dict
from enum import Enum
from .custom_errors import NegativeValueError


class SkillName(Enum):
    """
    a database representing different types of skills in the Arkham Horror available.
    """

    COMBAT = "combat"
    LORE = "lore"
    WILL = "will"
    LUCK = "luck"
    OBSERVATION = "Observation"


class Skill:
    """
    Class representing a skill in the Arkham Horror game.
    """

    _name: SkillName
    __skill_levels: Dict[SkillName, int]

    def __new__(cls, name: SkillName, level: int) -> Self:
        """
        :meth:`__new__` of :cls:`Skill` creates a new instance of Skill with the specified name and level. It sets the skill levels inside of :attr:`__skill_levels` to 0. It then returns the newly created instance.

        """
        self = super().__new__(cls)
        self._name = name
        self.__skill_levels = {
            SkillName.COMBAT: 0,
            SkillName.LORE: 0,
            SkillName.WILL: 0,
            SkillName.LUCK: 0,
        }
        self.__skill_levels[name] = level
        return self

    @property
    def name(self) -> SkillName:
        return self._name

    def level(self, skill: SkillName) -> int:
        """
        retrieves the skill level from the dictionary
        """
        if skill not in self.__skill_levels:
            raise KeyError(f"Skill {skill} cannot be found.")
        return self.__skill_levels[skill]

    def improve(self, skill: SkillName, amount: int) -> None:
        """
        Improves the skill level by a specified amount.
        """
        if amount <= 0:
            raise NegativeValueError(amount)
        if skill not in self.__skill_levels:
            raise KeyError(f"Skill {skill} cannot be found.")
        self.__skill_levels[skill] += amount

    def reduce(self, skill: SkillName, amount: int) -> None:
        """
        Reduces the skill level by a specified amount.
        """
        if amount <= 0:
            raise NegativeValueError(amount)
        if skill not in self.__skill_levels:
            raise KeyError(f"Skill {skill} cannot be found.")
        new_level = self.__skill_levels[skill] - amount
        if new_level < 0:
            raise NegativeValueError(new_level)
        self.__skill_levels[skill] = new_level

    def __repr__(self) -> str:
        """
        dunder method for pretty string representation of :cls:`Skill` attributes
        """
        return (
            f"Skill(name={self._name}, level={self.__skill_levels[self._name]})"
        )
