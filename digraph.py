"""
Implementation of Directed Graph. Ispired By: Dr. Stefano Gogioso. University of Oxford Object Oriented Programming Course, MSc Software Engineering Programme
"""

from collections.abc import Hashable, Set, MutableSet
from typing import TypeVar, Generic, Self


NodeT = TypeVar("NodeT", bound=Hashable)
Edge = tuple[NodeT, NodeT]


class DiGraph(Generic[NodeT]):
    """
    A custom implementation of a generic directed graph with operations such as adding node and adding edges. The class is desined to work with Hahasble items.
    """

    _nodes: MutableSet[NodeT]
    _edges: MutableSet[Edge[NodeT]]

    def __new__(cls) -> Self:
        self = super().__new__(cls)
        self._nodes = set()
        self._edges = set()
        return self

    @property
    def nodes(self) -> Set[NodeT]:
        return self._nodes

    @property
    def edges(self) -> Set[Edge[NodeT]]:
        return self._edges

    def add_node(self, node: NodeT) -> None:
        """
        adds a node to the graph
        """
        self._nodes.add(node)

    def add_edge(self, tail: NodeT, head: NodeT) -> None:
        """
        Adds a directed edge to the graph from a starting node to an ending node.
        """
        self._edges.add((tail, head))
        self._nodes.add(tail)
        self._nodes.add(head)


class PartialOrder(DiGraph[NodeT]):
    """
    A class representing a partial order (a directed acyclic graph) with some additional constraints such as preventing formation of cycles. Inherits from parent class :cls:`DiGraph`
    """

    def add_node(self, node: NodeT) -> None:
        super().add_node(node)

    def add_edge(self, tail: NodeT, head: NodeT) -> None:
        if self._creates_cycle(tail, head):
            raise ValueError(
                "Adding this edge creates a cycle, which is not allowed in a partial order."
            )
        super().add_edge(tail, head)

    def _creates_cycle(self, tail: NodeT, head: NodeT) -> bool:
        """
        Checks whether adding an edge from the `tail` node to the `head` node would create a cycle in the graph.

        Args:
            tail (NodeT): The node where the edge starts.
            head (NodeT): The node where the edge ends.

        Returns:
            bool: True if adding the edge would create a cycle, False otherwise.
        """
        visited = set()
        stack = [head]
        while stack:
            node = stack.pop()
            if node == tail:
                return True
            if node in visited:
                raise AttributeError(
                    "{node} is in {visited} and cannot be added"
                )

            visited.add(node)
            neighbors = [h for t, h in self._edges if t == node]
            stack.extend(neighbors)
        return False
