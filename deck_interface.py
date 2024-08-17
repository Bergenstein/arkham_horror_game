"""
The ABC that provides an interface for clients. It provides a number of abstract methods for shuffling, drawing, and adding cards to the deck. Subclasses are required to override these methods with their own logic. 
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TypeT = TypeVar("TypeT")


class Deck(ABC, Generic[TypeT]):
    """
    Defines an abstract base class Deck, representing a generic deck of cards. It is parameterized by a type variable TypeT to represent a deck of any type.
    """

    @abstractmethod
    def shuffle(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw_front(self) -> TypeT:
        raise NotImplementedError

    @abstractmethod
    def draw_rear(self) -> TypeT:
        raise NotImplementedError

    @abstractmethod
    def add_card_front(self, card: TypeT) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_card_rear(self, card: TypeT) -> None:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError
