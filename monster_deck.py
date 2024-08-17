"""
module that manages creation of a deck of monsters. It has a Single class MonsterDeck that inherits from Deck and includes an internal instance of Deque for card management.
"""

from .deck_interface import Deck
from .monster import Monster
from .deque import Deque
import random


class MonsterDeck(Deck[Monster]):
    """
    :cls:`MonsterDeck` handles operations relevant to creating a deck of monster cards. This class inherits from :cls:`Deck`. It stores the monster cards in a double-ended queue.
    """

    _cards: Deque[Monster]

    def __init__(self) -> None:
        """
        Initializes a new instance of :cls:`MonsterDeck` with an empty deck of monster cards.
        """
        self._cards = Deque[Monster]()

    def shuffle(self) -> None:
        """
        Shuffles the monster cards in the deck in-place.
        """
        cards = list(self._cards)  # converts the deque to a list
        random.shuffle(cards)  # shuffles the list
        self._cards = Deque(cards)  # converts back to deque

    def draw_front(self) -> Monster:
        """
        draws a monster card from the front of the monster deck if not empty.
        """
        return self._cards.dequeue_front()

    def draw_rear(self) -> Monster:
        """
        draws a monster card from the back of the monster deck if not empty.
        """
        return self._cards.dequeue_rear()

    def add_card_front(self, card: Monster) -> None:
        """
        adds a monster card to the front of the monster deck.
        """
        self._cards.enqueue_front(card)

    def add_card_rear(self, card: Monster) -> None:
        """
        adds a monster card to the rear of the monster deck.
        """
        self._cards.enqueue_rear(card)

    def __len__(self) -> int:
        """
        dunder method that returns the number of monster cards in the deck.
        """
        return len(self._cards)
