"""
This module contains the :cls:`Game`. It serves as the main facade for the Arkham Horror game. It encapsulates (hide the complexities of) the management of investigators, monsters, spaces, decks, game flow, as well as other components, providing a simple interface to clients to interact with the game.
"""

from .investigator import Investigator
from .space import Space
from .encounter_deck import EncounterDeck
from .event_deck import EventDeck
from .monster_deck import MonsterDeck
from .monster import Monster
from .mythos_cup import MythosCup
from .arkham_horror import (
    GameSetup,
    ActionManager,
    GameFlowManager,
    InvestigatorManager,
    SpaceManager,
)
from .event_deck import EventCard
from .mythos_token import MythosToken

from typing import List, Tuple, Optional, TYPE_CHECKING, Any


class Game:
    """
    The Game Facade exposed to the outside clients
    """

    _inv_manager: InvestigatorManager
    _loc_manager: SpaceManager
    _encounter_deck: EncounterDeck
    _event_deck: EventDeck
    _monster_deck: MonsterDeck
    _mythos_cup: MythosCup

    def __init__(self) -> None:
        """
        Initializes a new instance of the Game class, setting up the game environment by creating managers for investigators, locations (Space), decks (encounter, event, monster), and overall game flow mechanics. :meth:`__init__` creates instances of InvestigatorManager, SpaceManager, EncounterDeck, EventDeck, MonsterDeck, and MythosCup. It then uses the aforementioned instances to initialize GameSetup and ActionManager.

        """
        self._inv_manager = InvestigatorManager()
        self._loc_manager = SpaceManager()
        self._encounter_deck = EncounterDeck()
        self._event_deck = EventDeck()
        self._monster_deck = MonsterDeck()
        self._mythos_cup = MythosCup()

        self.game_setup = GameSetup(
            self._loc_manager,
            self._inv_manager,
            self._encounter_deck,
            self._event_deck,
            self._monster_deck,
            self._mythos_cup,
        )
        self.action_manager = ActionManager(
            self._inv_manager, self._loc_manager, self._encounter_deck
        )
        self.game_flow_manager = GameFlowManager(self.action_manager)

    def setup_game(
        self, locations: List[Space], candidate_connec: List[Tuple[str, str]]
    ) -> None:
        """
        sets up the game
        """
        self.game_setup.setup_game(locations, candidate_connec)

    def add_nodes(self, space: Space) -> None:
        """
        adds locations to the graph representing the game
        """
        self._loc_manager.add_space(space)

    def add_investigator(self, investigator: Investigator) -> None:
        """
        adds investigators to the game
        """
        self._inv_manager.add_investigator(investigator)

    def connect_spaces(self, space1_name: str, space2_name: str) -> None:
        """
        connecs locations
        """
        self._loc_manager.connect_spaces(space1_name, space2_name)

    def perform_action_inv(
        self, investigator_name: str, action: str, *args: Any
    ) -> None:
        """
        performs actions for a given investigator
        """
        # NOTE: The `*args` parameter is annotated with `Any`. This is because this method is quites compelx and needs to be able handle a lot of possible argument types, which depend on the specific action.
        # Different actions require different numbers, and indeed
        # different types of arguments (for example: a move action may require a Space object, but an attack action may require a Monster object, among many more args, etc). So, I have used `Any` in order to allow for this flexibility.  This is the same justification as in `arkam_horro.py` module. See: `arkam_horro.py:278-290`
        self.action_manager.perform_investigator_action(
            investigator_name, action, *args
        )

    def play_game_round(self) -> None:
        """
        plays a round of the game
        """
        self.game_flow_manager.play_round()

    def draw_event(self) -> Optional[EventCard]:
        """
        draws an event card from the front of the event deck
        """
        return (
            self._event_deck.draw_front()
        )  # draws the front event card from the deck For some cases like spawning clues or gate bursts (according to game rules)

    def draw_event_doomspread(self) -> Optional[EventCard]:
        """
        draws a spread doom event card from rear of the event deck
        """
        return (
            self._event_deck.draw_rear()
        )  # draws the read event card from the deck for spreading doom, according to game rules

    def draw_monster(self) -> Monster:
        """
        draws a monster from the monster deck
        """
        return self._monster_deck.draw_rear()  # For spawning monsters

    def draw_mythos_token(self) -> MythosToken:
        """
        draws a mythos token from the mythos cup
        """
        return self._mythos_cup.draw_token()
