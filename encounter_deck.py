"""
This module defines classes and routines for managing encounter cards in the Arkham Horror Game. It has the following classes:

1. StratEncounterEffect: Abstract base class that defines strategies for various encounter effects from rules of Game of Horror. 
2. StrategyTakeDamage: Strategy Pattern for applying damage encounter effect to an investigator 
3. StrategyLoseSanity:  Strategy Pattern for applying horror encounter effect to an investigator so that they lose their sanity.
4. StrategyGainItem: Strategy Pattern for applying ItemGain encounter effect to an investigator 
5. EncounterEffect: Enum to encapsulate different encounter effects.
6. EncounterCard: Represents a card used during encounters in Arkham Horror. It applies the correct strategy based on the effect.
7. EncounterDeck: handles operations relevant to a Deck of Encounters. It uses an internal Deque for card storage.
"""

from .deck_interface import Deck
from .deque import Deque
import random
from typing import TYPE_CHECKING, Any, Self, Union
from enum import Enum
from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from .item import Item

if TYPE_CHECKING:
    from .investigator import Investigator
    
else:
    Investigator = Any


EncounterResult = Union[int, Item]


class StratEncounterEffect(ABC):
    """
    defines an ABC with blueprint for an abstract :meth:`apply` that must be overridden by subclasses that inherit from :cls:`StratEncounterEffect`
    """

    @abstractmethod
    def apply(
        self, investigator: Investigator, value: int
    ) -> MutableMapping[str, EncounterResult]: ...


class StrategyTakeDamage(StratEncounterEffect):
    """
    Strategy Pattern for applying damage encounter effect to an investigator
    """

    def apply(
        self, investigator: Investigator, value: int
    ) -> MutableMapping[str, EncounterResult]:
        """
        Applies strategy pattern, causing the investogator to get hit with a specified amount of damage.
        """
        investigator.status.take_damage(
            value
        )  # delegates to InvestigatorStatus
        res: MutableMapping[str, EncounterResult] = {"health": -value}
        return res


class StrategyLoseSanity(StratEncounterEffect):
    """
    Strategy Pattern for applying horror encounter effect to an investigator so that they lose their sanity.
    """

    def apply(
        self, investigator: Investigator, value: int
    ) -> MutableMapping[str, EncounterResult]:
        """
        Applies strategy pattern, causing the investogator to get hit with a specified amount of horror to their sanity.
        """
        investigator.status.lose_sanity(
            value
        )  # delegates to InvestigatorStatus
        res: MutableMapping[str, EncounterResult] = {"sanity": -value}
        return res


class StrategyGainItem(StratEncounterEffect):
    """
    Strategy Pattern for applying ItemGain encounter effect to an investigator
    """

    def apply(
        self, investigator: Investigator, value: int
    ) -> MutableMapping[str, EncounterResult]:
        """
        Applies strategy pattern, causing the investogator to gain a specified value of a certain item that gets added to their invetory
        """
        item_new = Item(
            f"Item {value}",
            description=f"Item gain from encounter",
            effect="gain_item",
            amount=1,
        )
        investigator._inv_items.add_item(
            item_new
        )  # delegates to InvestigatorItems
        res: MutableMapping[str, EncounterResult] = {"item": item_new}
        return res


class EncounterEffect(Enum):
    """
    :cls:`EncounterEffect` inherits from Enum (collection of name-value pairs). It represents 4 different effects that can happen to game characters (investigators) during an encounter course in Arkham Horror.
    """

    TAKE_DAMAGE = "take_damage"
    LOSE_SANITY = "lose_sanity"
    GAIN_ITEM = "gain_item"
    GAIN_CLUE = "gain_clue"


class EncounterCard:
    """
    Represents a card used during encounters in Arkham Horror.
    """

    _description: str
    _effect: EncounterEffect
    _val: int
    _strategy: StratEncounterEffect

    def __new__(
        cls, description: str, effect: EncounterEffect, value: int
    ) -> Self:
        """
        :meth:`__new__` creates a fresh instance of the :cls:`EncounterCard`, initializes its attributes and returns that newly created and initialized instance.
        """
        self = super().__new__(cls)
        self._description = description
        self._effect = effect
        self._val = value
        if effect == EncounterEffect.TAKE_DAMAGE:
            self._strategy = StrategyTakeDamage()
        elif effect == EncounterEffect.LOSE_SANITY:
            self._strategy = StrategyLoseSanity()
        elif effect == EncounterEffect.GAIN_ITEM:
            self._strategy = StrategyGainItem()
        elif effect == EncounterEffect.GAIN_CLUE:
            ...

        return self

    def resolve_encounter(
        self, investigator: Investigator
    ) -> MutableMapping[str, Any]:
        """
        :meth`resolve_encounter`resolves an encounter for an investigator and returns a mapping that contain description, effect, value, and changes that happened during the encounter resolution.

        """
        # I have used any in here to provide flexibility as there are many different items
        # that can be values of the keys in the mapping:
        # - "description" is a str
        # - "effect" is an EncounterEffect enum
        # - "value" is an integer
        # - "changes" which can vary, depending on the strategy employed; it could be an `Item`, an int, etc.
        res: MutableMapping[str, Any] = {
            "description": self._description,
            "effect": self._effect,
            "value": self._val,
            "changes": self._strategy.apply(investigator, self._val),
        }
        return res

    def __repr__(self) -> str:
        """
        pretty string representation
        """
        return f"EncounterCard(description={self._description})"


class EncounterDeck(Deck[EncounterCard]):
    """
    Class that handles operations relevant to a Deck of Encounters. It inherits from the Deck class and uses an interal Deque to store the encounter cards.
    """

    _cards: Deque[EncounterCard]

    def __init__(self) -> None:
        """
        Initializes a new instance of the `EncounterDeck` class.

        This constructor initializes the `_cards` attribute of the `EncounterDeck` object to an empty `Deque` of `EncounterCard` objects.
        """
        self._cards = Deque[EncounterCard]()

    def shuffle(self) -> None:
        """
        Shuffles the cards in the encounter deck.
        """
        cards = list(self._cards)
        random.shuffle(cards)
        self._cards = Deque(cards)

    def draw_front(self) -> EncounterCard:
        """deques front of EncounterDeck, extracting an EncounterCard"""
        return self._cards.dequeue_front()

    def draw_rear(self) -> EncounterCard:
        """deques rear of EncounterDeck, extracting an EncounterCard"""
        return self._cards.dequeue_rear()

    def add_card_rear(self, card: EncounterCard) -> None:
        """adds an EncounterCard to rear of an EncounterDeck"""
        self._cards.enqueue_rear(card)

    def add_card_front(self, card: EncounterCard) -> None:
        """adds an EncounterCard to front of an EncounterDeck"""
        self._cards.enqueue_front(card)

    def __len__(self) -> int:
        """implements __len__ dunder"""
        return len(self._cards)
