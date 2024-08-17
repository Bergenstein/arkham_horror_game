"""
This module deals with the implementation of spell effects cast by an investigator in Arkham Horror. This module provides a base class, `SpellEffect`. This base class serves as a template for all specific spell effects in the game. 

Subclasses inherit from `SpellEffect` base class and override `apply` method of the base class by providing their own specific implementations of the spell effects. 
"""

from typing import TYPE_CHECKING
from .space import Space
from .investigator import Investigator


class SpellEffect:
    """
    :cls:`SpellEffect` represents a generic spell effects in Arkham Horror:
    it: 1. defines a common interface for spell effect. 2. provides a static validation method.
    """

    @staticmethod
    def validate_args(investigator: Investigator) -> None:
        """
        :meth:`validate_args` Validates the arguments for applying a spell effect.
        It checks: 1. if the investigator is engaged with any monsters 2. if the investigator is able to cast spell. With health and sanity not being positive, investigator is dead and prevented from casting spell.
        """
        if not investigator.engaged_monsters:
            raise ValueError("No monster found to engage with.")
        if investigator.status.health <= 0 or investigator.status.sanity <= 0:
            raise AttributeError(
                "Investigator is dead and unable to cast spells."
            )

    def apply(self, investigator: Investigator, loc: Space) -> None:
        """
        apply method that needs to be overridden by subclasses
        """
        raise NotImplementedError(
            "This method must be overridden by subclasses."
        )


class HealEffect(SpellEffect):
    """
    :cls:`HealEffect`inherits from :cls:`SpellEffect`. This class represents a specific type of spell effect that heals an investigator but comes at increasing their horror attribute.
    """

    def apply(self, investigator: Investigator, loc: Space) -> None:
        """
        Applies the HealEffect spell effect to an investigator at a specific location.
        It first checks if investigator can apply this legally by calling parents :meth:`validate_args`. If that checks, it increases health's investigator's health attribute by 2 point while increasing investigator's horror attribute by 1 point. Oh yeah. Nothing in life comes free, not even in a game :)
        """
        SpellEffect.validate_args(
            investigator
        )  # delegate to SpellEffect to validate args
        investigator.status.heal(2)  # delegate to investigator status to heal
        investigator.assign_horror(
            1
        )  # delegate to investigator to assign horror


class BoostSanityEffect(SpellEffect):
    """
    :cls:`BoostSanityEffect`inherits from :cls:`SpellEffect`. This class represents a specific type of spell effect that boost an investigator's sanity but comes at increasing their horror attribute.
    """

    def apply(self, investigator: Investigator, loc: Space) -> None:
        """
        Applies the BoostSanityEffect spell effect to an investigator at a specific location. It first checks if investigator can apply this legally by calling parents :meth:`validate_args`. If that checks, it restores investigator's sanity attribute by 2 points while increasing investigator's horror attribute by 1 point. Oh yeah. Nothing in life comes free, not even in a game :)
        """
        SpellEffect.validate_args(investigator)
        investigator.status.restore_sanity(2)
        investigator.assign_horror(1)


class DamageMonsterEffect(SpellEffect):
    """
    :cls:`DamageMonsterEffect`inherits from :cls:`SpellEffect`. This class represents a specific type of spell effect that damages a monster's health but comes at increasing the horror attribute of investigator.
    """

    def apply(self, investigator: Investigator, loc: Space) -> None:
        """
        Applies DamageMonsterEffect spell effect to an investigator at a specific location. It first checks if investigator can apply this legally by calling parents :meth:`validate_args`. If that checks, it hits monster's health attribute by 2 points while increasing investigator's horror attribute by 1 point.
        """
        SpellEffect.validate_args(
            investigator
        )  # delegate to SpellEffect to validate args
        monster = investigator.engaged_monsters[0]  # retrieves the 1st monster
        monster.take_damage(2)  # hits the monster's health
        investigator.assign_horror(1)  # gets spell consequences
        if (
            monster.is_defeated()
        ):  # remove the monster from the engaged monsters if monster is defeated
            investigator.engaged_monsters.remove(monster)
