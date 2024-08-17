"""
This module manages interactions with tokens within Arkham Horror. 
It includes one class: 'TokensInteractions' which facilitates interactions between tokens (event, encounter) and other game components such as the investigators, the Mythos Cup and the monster. This module has methods to support different drawing operations. Validations are performed centrally to prevent illegal actions. 
"""

from .event_deck import EventCard
from .encounter_deck import EncounterCard

from typing import TYPE_CHECKING, Optional, Any
from .monster import Monster
from .mythos_cup import MythosCup

if TYPE_CHECKING:
    from .investigator import Investigator

else:
    Investigator = Any


class TokensInteractions:
    """
    :cls:`TokensInteractions` facilitates interactions between tokens (event, encounter) and other game components such as investigators, the Mythos Cup, and monsters in the Arkham Horror game.
    """

    _investigator: Investigator
    _cup: MythosCup

    def __init__(self, investigator: Investigator, cup: MythosCup):
        """
        :meth:`__init__` Initializes TokensInteractions with the given :attr:`investigator`and :attr:`MythosCup`.
        """
        self._investigator = investigator
        self._cup = cup

    @property
    def cup(self) -> MythosCup:
        return self._cup

    def draw_token(self) -> None:
        """
        Draws tokens from the Mythos Cup during the Mythos Phase
        Each investigator can draw two tokens and resolve their effects after checking validation.
        """
        if (
            self._cup.__size__() < 2
        ):  # further validation on top of the standard validation of the :meth: `draw_token` of the :cls:`MythosCup` which checks if the pool is empty through :cls:`Deque`.
            raise ValueError(
                "the cup needs to have at least 2 mythos inside to draw"
            )
        for _ in range(2):
            token = self._cup.draw_token()
            self._cup.execute_command(token.type)

    def draw_monster(self) -> Monster:
        """
        Draws a monster from the monster deck but first checks if the deck is empty.
        """
        return self._investigator.monster_deck.draw_front()

    def draw_event_token(self) -> Optional[EventCard]:
        """
        Draws an event token from the event deck but first checks if the deck is empty.
        Validation is the responsibility of the :cls:`Deque`
        """
        # if len(self._investigator._inv_items._event_deck) == 0:
        #     raise ValueError("the deck {self._event_deck} is empty")
        return self._investigator._inv_items._event_deck.draw_front()

    def draw_encounter_token(self) -> Optional[EncounterCard]:
        """
        Draws an encounter token from the encounter deck but first checks if the deck is empty. Validation is the responsibility of the :cls:`Deque`
        """
        return self._investigator._inv_items._encounter_deck.draw_front()
