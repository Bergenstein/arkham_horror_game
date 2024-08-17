"""
This module is responsible for Mythons tokens. 
"""

from typing import Literal

# All possible types of Mythos tokens from the game descriptions. Literal has been used for type safety
TokenType = Literal[
    "spread_doom",
    "spawn_monster",
    "read_headline",
    "spawn_clue",
    "gate_burst",
    "reckoning",
    "blank",
]


class MythosToken:
    """
    a simple data container that represents a token with a specific type of type: `TokenType`.
    """

    _type: TokenType  # one of the LiteralType defined above

    def __init__(self, token_type: TokenType):
        self._type = token_type

    def __repr__(self) -> str:
        """
        dunder method for pretty printing and string representation of a mythos object
        """
        return f"MythosToken(type={self._type})"

    @property
    def type(self) -> TokenType:
        return self._type
