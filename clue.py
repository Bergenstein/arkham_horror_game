"""
This module deals with clues within Arkham Horror Game. Clues have attributes such as id, description and put on locations according to game rules.
"""

from .space import Space
class Clue:
    """
    represents clues in Arkham Horror game. Each clue has three attributes :attr:`location`, :attr:`description` and :attr:`clue_id`
    """

    _location: Space
    _description: str
    _clue_id: int

    def __init__(self, id: int, description: str, location: Space):
        """
        initializes the clue and sets its attributes
        """
        self._location = location
        self._description = description
        self._clue_id = id

    @property
    def location(self) -> Space:
        return self._location

    @property
    def description(self) -> str:
        return self._description

    @property
    def clue_id(self) -> int:
        return self._clue_id
