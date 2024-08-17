"""
The module implements logic as well as core components for playing Arkham Horror. 
It includes multiple classes, each responsible to manage one component of the game such as: setup, investigators, spaces, decks, actions, as well as the game flow.

Components (all in their own classes):

1. GameSetup: Handles and deals with initial setup of Arkham Horror game.
2. InvestigatorManager: Manages investigators in the game.
3. SpaceManager: Manages locations and how they are connected in the game.
4. DeckActionHandler: Manages operations on decks of actions.
5. Action: A metaclass that auto-registers action methods.
6. ActionManager: Manages actions and action related activities for investigators within Arkham Horror.
7. GameFlowManager: Controls the flow of the game.
"""

from collections.abc import Iterable, Callable, Hashable, Mapping
from typing import (
    TypeVar,
    Generic,
    Type,
    Dict,
    List,
    Self,
    Any,
    Tuple,
    Sequence,
)
import random
from .space import Space
from .investigator import Investigator
from .monster import Monster
from .encounter_deck import EncounterDeck
from .event_deck import EventDeck
from .monster_deck import MonsterDeck
from .mythos_cup import MythosCup
from .digraph import DiGraph
from .clue import Clue
from .custom_errors import NotFoundError

NodeT = TypeVar("NodeT", bound=Hashable)


class GameSetup:
    """
    :cls:`GameSetup`: Initializes and sets up a game of Arkham Horror.

    The GameSetup class is responsible for initial setup and preparaion the Arkham Horror game environment. It does it though shuffling decks (event, monster and encounter), replenishing mythos cup, adding and conncting locations (spaces).
    """

    ...
    _space_manager: "SpaceManager"
    _investigator_manager: "InvestigatorManager"
    _encounter_deck: EncounterDeck
    _event_deck: EventDeck
    _monster_deck: MonsterDeck
    _mythos_cup: MythosCup

    def __new__(
        cls,
        space_manager: "SpaceManager",
        investigator_manager: "InvestigatorManager",
        encounter_deck: EncounterDeck,
        event_deck: EventDeck,
        monster_deck: MonsterDeck,
        mythos_cup: MythosCup,
    ) -> Self:
        """
        Constructor that creates an instance of GameSetUp class
        """
        self = super().__new__(cls)
        self._space_manager = space_manager
        self._investigator_manager = investigator_manager
        self._encounter_deck = encounter_deck
        self._event_deck = event_deck
        self._monster_deck = monster_deck
        self._mythos_cup = mythos_cup
        return self

    def setup_game(
        self, locations: List[Space], loc_to_conn: Sequence[Tuple[str, str]]
    ) -> None:
        """
        Method responsible for game setup in :cls:`GameSetup` via:
            1. shuffling encounter, event, and monster decks
            2. replenishing the mythos cup
            3. adding and connection locations.
        """
        self._encounter_deck.shuffle()
        self._event_deck.shuffle()
        self._monster_deck.shuffle()
        self._mythos_cup.replenish()

        if not locations:
            raise ValueError("No locations found")
        if not loc_to_conn:
            raise ValueError(
                "No connections possible as there are no {loc_to_conn}"
            )

        for loc in locations:
            self._space_manager.add_space(loc)  # adds a location

        for space1_name, space2_name in loc_to_conn:  # connects two locations
            self._space_manager.connect_spaces(space1_name, space2_name)

        for investigator in self._investigator_manager._investigators.values():
            self._space_manager.add_space(
                investigator.location
            )  # puts an investigator on that location


class InvestigatorManager:
    """
    :cls:`InvestigatorManager` manages investigator related methods such as creating a dictionary of investigators and having methods to add investigatord and retrieve them from the dictionary.
    """

    _investigators: Dict[str, Investigator]

    def __init__(self) -> None:
        self._investigators = {}

    def add_investigator(self, investigator: Investigator) -> None:
        """
        adds investigators to investigators dictionary.
        """
        self._investigators[investigator.name] = investigator

    def get_investigator(self, name: str) -> Investigator:
        """
        retrieves an investigator. Raises a KeyError if the investigator doesn't exist
        """
        if name not in self._investigators.keys():
            raise KeyError(
                "the investigator {name} doesn't exit in {self._investigator}"
            )
        return self._investigators[name]

    @property
    def investigators(self) -> Dict[str, Investigator]:
        return self._investigators


class SpaceManager:
    """
    class responsible for managing locations:  adding, connecting and retreiving the location objects.
    """

    _graph: DiGraph[Space]
    __spaces: Dict[str, Space]

    def __init__(self) -> None:
        """
        Initializes a new instance of :cls:`SpaceManager`.

        Sets up the internal graph and spaces to manage spaces in the game.
        """
        self._graph = DiGraph[Space]()
        self.__spaces = {}

    def add_space(self, loc: Space) -> None:
        """
        Adds a new location as a node to the graph that represent the game structure. Also, adds the space to the spaces Dict.
        """

        self._graph.add_node(loc)
        self.__spaces[loc.name] = loc

    def connect_spaces(self, space1_name: str, space2_name: str) -> None:
        """
        uses the add_edge method of the graph to connect two locations
        """
        loc1: Space = self.__spaces[space1_name]
        loc2: Space = self.__spaces[space2_name]

        self._graph.add_edge(loc1, loc2)

    def get_space(self, name: str) -> Space:
        """
        a getter method that retrieve a Space object from the dictionary of spaces
        """
        return self.__spaces[name]


itemT = TypeVar("itemT")


class DeckActionHandler(Generic[itemT]):
    """
    Responsible for managing a deck of items. :cls:`DeckActionHandler` provides methods for shuffling, drawing items from the front and rear as well as adding items to the front and rear. Uses List for convenience of opretaions.

    """

    _elems: List[itemT]  # a list of elements

    def __init__(self, elem: Iterable[itemT]) -> None:
        self._elems = list(elem)

    def shuffle(self, shuffle_func: Callable[[List[itemT]], None]) -> None:
        """
        Shuffles the items by calling a shuffling function `shuffle_func`.
        """
        shuffle_func(self._elems)

    def draw_front(self) -> itemT:
        """
        takes elems from front of the list
        """
        return self._elems.pop(0)

    def draw_rear(self) -> itemT:
        """
        takes elems from read of the list
        """
        return self._elems.pop()

    def add_card_rear(self, card: itemT) -> None:
        """
        appends elems to rear of list
        """
        self._elems.append(card)

    def add_card_front(self, card: itemT) -> None:
        """
        appens elems to front of list
        """
        self._elems.insert(0, card)

    def __len__(self) -> int:
        """dunder method that returns length of elems list"""
        return len(self._elems)


elemT = TypeVar("elemT", bound="Action")


class Action(type):
    """
    :cls:`Action` is a metaclass that auto registers methods starting with _action in a dictionary called _registered_actions when a new class is created using this metaclass.
    """

    _registered_actions: Mapping[str, Callable[..., Any]]

    def __new__(
        cls: Type[elemT],
        name: str,
        bases_tup: Tuple[Type[elemT], ...],
        dic_vals: Dict[str, elemT],
    ) -> elemT:
        """
        Creates a new class using the provided name, bases_tup (a Tuple[Type, ...]), and dictionary values.

        :meth:`__new__` is a metaclass constructor, initializing a new class and
        automatically registers methods starting with '_action' in a dictionary
        called _registered_actions.

        Returns:
            elemT: The newly created class.
        """

        new_cls = super().__new__(cls, name, bases_tup, dic_vals)

        # init _registered_actions dictionary
        new_cls._registered_actions = {}

        # Populate _registered_actions with any method that with '_action'
        for key, value in dic_vals.items():
            if callable(value) and key.startswith("_action"):
                new_cls._registered_actions[key] = value

        return new_cls


class ActionManager(metaclass=Action):
    """
    :cls:`ActionManager`: handles managing and executing actions
    performed by investigators in Arkham Horror game. :cls:`ActionManager` uses :cls:`Action` metaclass to auto-register and manage action methods.

    """

    investigator_manager: InvestigatorManager
    space_manager: SpaceManager
    encounter_deck: EncounterDeck

    def __new__(
        cls,
        investigator_manager: InvestigatorManager,
        space_manager: SpaceManager,
        encounter_deck: EncounterDeck,
    ) -> Self:
        """
        :meth:`__new__` is the constructor responsible for creating new instance of :cls:`ActionManager`. It initializes :attr:`_investigator_manager`, :attr:`_space_manager` and :attr:`_encounter_deck` and returns the newly created and initialized instance of the class.
        """
        self = super().__new__(cls)
        self.investigator_manager = investigator_manager
        self.space_manager = space_manager
        self.encounter_deck = encounter_deck
        return self

    def get_action_map(self) -> Dict[str, Callable[..., Any]]:
        """
        :meth:`get_action_map` of :cls:`ActionManager` returns a dictionary mapping action names: str to their corresponding functions.
        """
        return {
            key.replace("_action", ""): func
            for
            # # MyPy raises an "attr-defined" error here because it doesn't recognize that `_registered_actions`
            # is dynamically added by the metaclass `Action` that handles the actual creation of this attribute,
            # so it is present at runtime, but not visible to MyPy.
            key, func in self._registered_actions.items()# type: ignore
        }  

    def perform_investigator_action(
        self, investigator_name: str, action: str, *args: Any
    ) -> None:
        """
        :meth:`perform_investigator_action` is responsible for an investigator action in Arkham Horror. It raises an error if the action is not found in the action map.
        For Example: To move an investigator named "Lakshmi Patel" to a new space such as "Downtown" we perform the action like that:

        perform_investigator_action("Lakshmi Patel", "move_investigator", "Downtown")
        """
        # NOTE: The `*args` parameter is annotated with `Any`. This is because this method is quites compelx and needs to be able handle a lot of possible argument types, which depend on the specific action.
        # Different actions require different numbers, and indeed
        # different types of arguments (for example: a move action may require a Space object, but an attack action may require a Monster object, among many more args, etc). So, I have used `Any` in order to allow for this flexibility.

        # retrieve an investigator from the investigator manager by looking up its name. Deletages retrieval to InvestigatorManager.
        investigator = self.investigator_manager.get_investigator(
            investigator_name
        )
        action_map = (
            self.get_action_map()
        )  # retreives an action from the action map

        action_func = action_map.get(
            action
        )  # gets the corresponding function to the action string and stores in variable action_func.
        if not action_func:
            raise NotFoundError(action, action_map)

        if action in ["draw_token", "draw_event_token", "draw_monster"]:
            action_func()  # simple action requiring passing no arguments. Just perform
        else:
            action_func(
                investigator, *args
            )  # more complex actions, requiring passing investigator and extra arguments.

    def _move_investigator(
        self, investigator: Investigator, new_space_name: str
    ) -> None:
        """
        moves an investigator to a new space.
        """
        new_space = self.space_manager.get_space(
            new_space_name
        )  # delegates to get_spaces method of SpaceManager
        investigator.move(
            new_space
        )  # delegates `move` method of `Investigator`

    def _attack_monster(
        self, investigator: Investigator, monster: Monster
    ) -> None:
        """
        investigator attacking a monster
        """
        investigator.attack_monster(
            monster
        )  # delegates to attack_monster method of Investigator

    def _evade_monster(
        self, investigator: Investigator, monster: Monster
    ) -> None:
        """
        logic handling an investigator evading a monster
        """
        investigator.evade_monster(
            monster
        )  # delegates to evade_monster method of Investigator

    def _ward_doom(self, investigator: Investigator) -> None:
        """
        Wards doom for the given investigator.
        """
        investigator.ward_doom()

    def resolve_encounter(self, investigator: Investigator) -> None:
        """
        Resolves an encounter action for the given investigator if there are no engaged monsters. According to Game rules, investigators can only resolve encounters if not engaged with monsters currently.
        """
        if not investigator.engaged_monsters:
            # draw an encounter card from front of encounter deck
            encounter_card = self.encounter_deck.draw_front()
            if not encounter_card:
                raise ValueError("No encounter card available.")

            encounter_card.resolve_encounter(investigator)


class GameFlowManager:
    """
    class that deals with the overall flow of the game of Arkham Horror such as getting actions from :cls:`DeckActionHandler` and using :cls:`ActionManager` to handle the retrieved action cards.
    """

    action_manager: ActionManager

    def __init__(self, action_manager: ActionManager) -> None:
        self.action_manager = action_manager

    def play_round(self) -> None:
        """
        Plays a round of Arkham Horror game, iterating over all investigators and performing actions drawn from the action deck.
        """

        for (
            investigator
        ) in self.action_manager.investigator_manager.investigators.values():
            # Get the action map
            action_map = self.action_manager.get_action_map()

            actions_deck = DeckActionHandler(list(action_map.keys()))

            # Shuffle the deck of actions
            actions_deck.shuffle(random.shuffle)

            # Draw actions one at a time and perform them as drawn
            while len(actions_deck) > 0:
                action = actions_deck.draw_front()
                self.action_manager.perform_investigator_action(
                    investigator.name, action
                )
