"""
This module defines the `Spell` class and its related attributes and methods for the Arkham Horror game. A spell can be cast by an investigator during the game and it can have adverse consequences for the investigator, increase their horror if cast. 
"""

from typing import TYPE_CHECKING, Any
from .space import Space
from .spell_effects import SpellEffect


if TYPE_CHECKING:
    from .investigator import Investigator
    
else:
    Investigator = Any


class Spell:
    """
    Class representing a spell in the Arkham Horror game.
    """

    _horror: int
    _name: str
    _effect: SpellEffect

    def __init__(self, name: str, effect: SpellEffect, horror: int = 0) -> None:
        """
        :meth:`__init__` initializes a Spell object with given name, effect, and horror value.
        """
        self._name = name
        self._effect = effect
        self._horror = horror

    @property
    def name(self) -> str:
        return self._name

    @property
    def effect(self) -> SpellEffect:
        return self._effect

    @property
    def horror(self) -> int:
        return self._horror

    def cast(self, investigator: Investigator, loc: Space) -> None:
        """
        Cast the spell via delegating it to :meth:`apply` method of :cls:`SpellEffect` which is then depending on what the effect is calls the relevant implementation of apply.
        """
        self._effect.apply(investigator, loc)  # delegates to SpellEffect class
