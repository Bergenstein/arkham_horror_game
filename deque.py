"""
Implementation of Queue, inspired by Dr. Stefano Gogioso's Implementation of Bag, University of Oxford Object Oriented Programming Course, MSc Software Engineering Programme
"""

from typing import Optional, Generic, TypeVar, Self, Iterator
from collections.abc import Hashable, Iterable

ItemT = TypeVar('ItemT', bound = Hashable)

class QueueNode(Generic[ItemT]):
    """
    A generic class that represents a node in a queue data structure.
    """
    _next: Optional["QueueNode[ItemT]"]
    _prev: Optional['QueueNode[ItemT]']
    _value: ItemT
    def __new__(cls, value: ItemT, 
                next_node: Optional['QueueNode[ItemT]'] = None, 
                prev_node: Optional['QueueNode[ItemT]'] = None) -> Self:
        """
        Initializes a new instance of the QueueNode class and returns the freshly created instance.

        """
        self = super().__new__(cls)
        self._value = value
        self._next = next_node
        self._prev = prev_node
        return self

    def __repr__(self) -> str:
        """
        returns a pretty string representation of the `QueueNode` object
        in the format of QueueNode(value={self._value})' .
        """
        return f'QueueNode(value={self._value})'

class Deque(Generic[ItemT]):
    """
    :cls:`Deque`is a custom implementation of Double-Ended Queue data structure. The class is designed so that it can work with hashable items. It supports operations such as addition and removal of nodes from front and rear. It supports composition by composing instances of :cls:`QueueNode` to utilize some of its methods.
    """
    __front_items: Optional[QueueNode[ItemT]]
    __rear_items: Optional[QueueNode[ItemT]]
    __size: int
    def __new__(cls, items: Iterable[ItemT] = ()) -> Self:
        """
        Initializes a new instance of the Deque class and returns the newly created Deque instance.
        """
        self = super().__new__(cls)
        self.__front_items = None
        self.__rear_items = None
        self.__size = 0
        for item in items:
            self.enqueue_front(item)
        return self

    def __repr__(self) -> str:
        return f'Deque(size={self.__size})'

    def __len__(self) -> int:
        return self.__size
    
    def __iter__(self) -> Iterator[ItemT]:
        """
        dunder method implementing iteration for the :cls:`Deque`
        """
        current = self.__front_items
        while current is not None:
            yield current._value
            current = current._next

    @property
    def front_items(self) -> Optional[QueueNode[ItemT]]:
        return self.__front_items
    
    @property 
    def rear_items(self) -> Optional[QueueNode[ItemT]]:
        return self.__rear_items
    @property 
    def size(self) -> int:
        return self.__size
    

    def dequeue_front(self) -> ItemT:
        """
        Dequeues an item from the front of the deque.
        """
        if self.is_empty():
            raise IndexError("dequeue from empty deque")
        
        # Explicitly checking that __front_items is not None
        if self.__front_items is None:
            raise RuntimeError("Deque internal state error: front item is None despite non-empty deque")
        
        item = self.__front_items._value  
        self.__front_items = self.__front_items._next  

        # Next node isn't none => setting its prev to None. 
        # By setting prev to none we are defacto removing the node 
        if self.__front_items is not None:
            self.__front_items._prev = None 
        else:
            self.__rear_items = None 
        
        self.__size -= 1
        
        return item

    def dequeue_rear(self) -> ItemT:
        """
        dequeues an item from rear of the deque
        """
        if self.is_empty():
            raise IndexError("dequeue from empty deque")
        if self.__rear_items is None:
            raise RuntimeError("Deque internal state error: rear item is None despite non-empty deque")

        item = self.__rear_items._value 
        self.rear = self.__rear_items._prev 
        if self.rear:
            self.rear._next = None
        else:
            self.front = None
        self.__size -= 1
        
        return item
    
    def enqueue_front(self, item: ItemT) -> None:
        """
        Enqueues an item at the front of the deque.
        """
        new_node = QueueNode(item)
    
        if self.is_empty():

            self.__front_items = self.__rear_items = new_node
        else:
            new_node._next = self.__front_items
            if self.__front_items:  # Check if front is not None
                self.__front_items._prev = new_node
            self.__front_items = new_node
        self.__size += 1

    def enqueue_rear(self, item: ItemT) -> None:
        """
        Enqueue an item at the rear of the deque.
        """
        new_node = QueueNode(item)

        if self.is_empty():
            self.__front_items = self.__rear_items = new_node
        else:

            new_node._prev = self.__rear_items
            if self.__rear_items:
                self.__rear_items._next = new_node
            self.__rear_items = new_node
        self.__size += 1


    def peek_front(self) -> ItemT:
        """
        checks front of deque.
        """
        if self.is_empty():
            raise IndexError("peek from empty deque")
        if self.__front_items is None:
            #extra validation for typechecker
            raise ValueError("cannot peak at front")
        return self.__front_items._value

    def peek_rear(self) -> ItemT:
        """checks rear of deque"""
        if self.is_empty():
            raise IndexError("peek from empty deque")
        if self.__rear_items is None:
            #extra validation for typechecker
            raise ValueError("cannot peak at rear")
        return self.__rear_items._value

    def is_empty(self) -> bool:
        return self.__front_items is None


