"""
module that manages creation of a deck of events. It has two classes EventCard and EventDeck which inherits from Deck of EventCard and includes an internal instance of Deque for card management.
"""

from .deck_interface import Deck
from .deque import Deque
import random
from typing import Self


class EventCard:
    """
    a basic class the encapsulates an event deck with a destription attribute
    """

    _description: str

    def __init__(self, description: str):
        self._description = description

    def __repr__(self) -> str:
        return f"EventCard(description={self._description})"


class EventDeck(Deck[EventCard]):
    """
    :cls:`EventDeck` handles operations relevant to creating a deck of event cards. This class inherits from :cls:`Deck`. It stores the event cards in a deque.
    """

    _cards: Deque[EventCard]

    def __new__(cls) -> Self:
        """
        constructor that creates a new instance of EvenDeck and intializes the cards attributes to an empty Deque of EventCards. It then returns the freshly created and initialized instance.
        """
        self = super().__new__(cls)
        self._cards = Deque[EventCard]()
        return self

    def shuffle(self) -> None:
        """
        Shuffles the event cards in the deck in-place.
        """
        cards = list(self._cards)
        random.shuffle(cards)
        self._cards = Deque(cards)

    def draw_front(self) -> EventCard:
        """
        draws event cards from front of event deck if not empty
        """
        return self._cards.dequeue_front()

    def add_card_rear(self, card: EventCard) -> None:
        """
        adds event cards to rear of deck
        """
        self._cards.enqueue_rear(card)

    def add_card_front(self, card: EventCard) -> None:
        """
        adds event cards to front of deck
        """
        self._cards.enqueue_front(card)

    def draw_rear(self) -> EventCard:
        """
        draws event cards from rear of event deck if not empty
        """
        return self._cards.dequeue_rear()

    def __len__(self) -> int:
        """
        dunder method that returns the number of event cards in the deck.
        """
        return len(self._cards)
