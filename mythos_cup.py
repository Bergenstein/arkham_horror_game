"""
This module defines the classes and their associated methods and attributes related to Mythos Cup in Arkham Horror. 

The MythosCup is responsible for managing Mythos tokens, their operations. It also manages execution of commands associated with the tokens and the Mythos Cup. The Mythos Cup uses the command design pattern to manage commands associated with mythos tokens.
"""

from .mythos_token import MythosToken, TokenType
from abc import ABC, abstractmethod
from typing import Dict, List


class Mythos_CMD(ABC):
    """
    ABC for Mythos commands. Subclasses must implement abstract method :meth:`execute`
    """

    @abstractmethod
    def execute(self) -> None:
        """
        This is an abstract method that must be implemented by subclasses.
        """
        ...


class MythosCup:
    """
    class responsible for setting up Mythos tokens and their related operations such as replenishing the cup, drawing tokens, executing commands, etc
    """

    _tokens: List[MythosToken]
    _commands: Dict[TokenType, Mythos_CMD]

    def __init__(self) -> None:
        """
        Initializes a new instance of :cls:`MythosCup` with empty tokens list and empty commands dictionary.
        """
        self._tokens = []
        self._commands = {}

    @property
    def tokens(self) -> List[MythosToken]:
        """
        Getter for _tokens.
        """
        return self._tokens

    @tokens.setter
    def tokens(self, tokens: List[MythosToken]) -> None:
        """
        Setter for _tokens.
        """
        self._tokens = tokens

    def __size__(self) -> int:
        return len(self.tokens)

    def draw_token(self) -> MythosToken:
        """
        Draws a token from the Mythos Cup.

        If there are tokens available in the cup, this method removes and returns the top token.

        If there are no tokens available, it raises an exception).

        """
        if self.__size__() == 0:
            raise ValueError("the mythos cup is empty")

        return self._tokens.pop()

    def replenish(self) -> None:
        """
        Replenish the tokens in the Mythos Cup with the list of mythos tokens
        """
        token_types: List[TokenType] = [
            "spread_doom",
            "spawn_monster",
            "read_headline",
            "spawn_clue",
            "gate_burst",
            "reckoning",
            "blank",
        ]

        self._tokens = [MythosToken(t) for t in token_types]

    def spread_doom(self) -> None:
        raise NotImplementedError

    def spawn_monster(self) -> None:
        raise NotImplementedError

    def read_headline(self) -> None:
        raise NotImplementedError

    def spawn_clue(self) -> None:
        raise NotImplementedError

    def gate_burst(self) -> None:
        raise NotImplementedError

    def reckoning(self) -> None:
        raise NotImplementedError

    def register_command(self, token: TokenType, command: Mythos_CMD) -> None:
        """
        Registers a command associated with a mythos token and adds the key-value mapping (token -> command) to the commands dictionary.

        """
        self._commands[token] = command

    def execute_command(self, token: TokenType) -> Mythos_CMD:
        """
        Executes a command associated with a mythos token using the Command Design Pattern
        """
        command = self._commands.get(
            token
        )  # retrieves the command from commands dictionary for a given token
        if command is None:
            raise ValueError("command doesnt exists")

        command.execute()  # command exists and now it can be executed
        return command


class Replenish(Mythos_CMD):
    """
    Command for replenishing the MythosCup. :cls:`Replenish` implements :meth:`execute`
    """

    _cup: MythosCup

    def __init__(self, cup: MythosCup) -> None:
        self._cup = cup

    def execute(self) -> None:
        self._cup.replenish()


class SpreadDoom(Mythos_CMD):
    """
    command for spreading doom. :cls:`SpeakDoom` implements :meth:`execute`
    """

    _cup: MythosCup

    def __init__(self, cup: MythosCup) -> None:
        self._cup = cup

    def execute(self) -> None:
        self._cup.spread_doom()


class SpawnMonster(Mythos_CMD):
    """
    command for Spawning Monster. :cls:`SpawnMonster` implements :meth:`execute`
    """

    _cup: MythosCup

    def __init__(self, cup: MythosCup) -> None:
        self._cup = cup

    def execute(self) -> None:
        self._cup.spawn_monster()


class ReadHeadline(Mythos_CMD):
    """
    command for Reading Headline. :cls:`ReadHeadline` implements :meth:`execute`
    """

    _cup: MythosCup

    def __init__(self, cup: MythosCup) -> None:
        self._cup = cup

    def execute(self) -> None:
        self._cup.read_headline()


class SpawnClue(Mythos_CMD):
    """
    command for Spawning Clue. :cls:`SpawnClue` implements :meth:`execute`
    """

    _cup: MythosCup

    def __init__(self, cup: MythosCup) -> None:
        self._cup = cup

    def execute(self) -> None:
        self._cup.spawn_clue()


class GateBurst(Mythos_CMD):
    """
    command for Bursting Gate. :cls:`GateBurst` implements :meth:`execute`
    """

    _cup: MythosCup

    def __init__(self, cup: MythosCup) -> None:
        self._cup = cup

    def execute(self) -> None:
        self._cup.gate_burst()


class Reckoning(Mythos_CMD):
    """
    command for Reckoning. :cls:`Reckoning` implements :meth:`execute`
    """

    _cup: MythosCup

    def __init__(self, cup: MythosCup) -> None:
        self._cup = cup

    def execute(self) -> None:
        self._cup.reckoning()


class Blank(Mythos_CMD):
    def execute(self) -> None:
        raise NotImplementedError
