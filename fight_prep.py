"""
This module is one of the core pieces of the game. Since investigator(s) is(are) the main character of the game with many complexities, this module has multiple classes that deal with various components, each doing their best to adhere to SOLID principles. 


Modules: 
1. `InvestigatorItems`: This class handles various paraphernalia at the disposal of the investigator. It only deals with such paraphernalia and resources. 
2. `InvestigatorTokens`: This class handles the operations allowed on the tokens available to the investigator; the addition, spending, and resetting of various tokens.
3. `Combat`: The combat class deals with fight-related actions that happen between investigator and monster, initialized by investigator. 
4. `InvestigatorSpells`: This class manages casting spells and any effect the spells would have on an investigator casting them. 
5. `Move`: The Move class handles how the investigator moves across the game board, going from location to location. 
6. `Trade`: This class is designed to handle the trade requirements of the game where the investigator trades paraphernalia at their disposal with their allies. 
7.`EncounterResolution`: When investigators are required to resolve encounters, this class is there to get a hold of that requirement of the game.
8. `InvCommand`: A base class for implementing the command design pattern

"""

from .monster import Monster
from .item import Item
from .skills import SkillName, Skill
from .spell import Spell
import random
from .event_deck import EventDeck
from .encounter_deck import EncounterDeck
import numpy as np
from .space import Space
from .clue import Clue
from .custom_errors import CustomError, NegativeValueError, NotFoundError
from .monster_deck import MonsterDeck
import math

from typing import (
    TYPE_CHECKING,
    Optional,
    Dict,
    List,
    Self,
    Literal,
    Self,
    cast,
    Protocol,
    Any,
)
from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from .investigator_status import InvestigatorStatus
from .investigator import BaseInvestigator, Investigator


Tokens = Literal[
    "horror_tokens",
    "focus_tokens",
    "money_tokens",
    "remnant_tokens",
    "clue_tokens",
    "doom_tokens",
    "activation_token",
]  # types of tokens used by investigator


class MoveAction(Protocol):
    """
    This class defines a protocol named MoveAction. It defines a blueprint for a single method :meth:`move` that subclasses must implement.
    """

    def move(self, space: Space) -> None: ...


class CombatAction(Protocol):
    """
    CombatAction protocol sets up the blueprint for 3 methods :meth:`attack_monster`, :meth:`ward_doom` and :meth:`evade_monster` that must be implemented by inheriting classes
    """

    def attack_monster(self, monster: Monster) -> None: ...
    def ward_doom(self) -> None: ...
    def evade_monster(self, monster: Monster) -> None: ...


class SpellAction(Protocol):
    """
    This class defines a protocol named SpellAction. It defines a blueprint for a single method :meth:`cast_spell` that subclasses must implement.
    """

    def cast_spell(self, spell: Spell, monster: Monster) -> None: ...


class TradeAction(Protocol):
    """
    This class defines a protocol named TradeAction, which defines a blueprint for a single method :meth:`trade` that subclasses that inherit from it must implement.
    """

    def trade(
        self,
        ally: Investigator,
        items: List[Item],
        spells: List[Spell],
        money: int,
        clues: List[Clue],
        remnants: int,
    ) -> None: ...


class EncounterAction(Protocol):
    """
    This class defines a protocol named EncounterAction, which defines a blueprint for a single method :meth:`resolve_encounter` that subclasses that inherit from it must implement.
    """

    def resolve_encounter(self) -> None: ...


class InvestigatorTokens:
    """
    :cls:`InvestigatorTokens` handles a set of tokens for an investigator in a game, allowing for adding, spending, and tracking token counts.
    """

    __focus_tokens: MutableMapping[
        str, int
    ]  # focus_tokens Mapping available to invstigator

    def __init__(self) -> None:
        self.__focus_tokens = {
            "horror_tokens": 0,
            "focus_tokens": 0,
            "money_tokens": 0,
            "remnant_tokens": 0,
            "clue_tokens": 0,
            "doom_tokens": 0,
            "activation_token": 0,
        }

    def _validate_operations(self, token_type: str) -> None:
        """performs validation to see if the key exists in the hashmap."""
        if token_type not in self.__focus_tokens:
            raise KeyError(f"Token type '{token_type}' not found")

    def add_token(self, token_type: str, amount: int) -> None:
        """
        increases the count of a token by a specified amount.
        First performs validation to see if the key exists in the hashmap.
        """
        self._validate_operations(token_type)
        self.__focus_tokens[token_type] += amount

    def spend_token(self, token_type: str, amount: int) -> None:
        """
        spend the token -> decreases the count of the token, its associated value in the mapping, by a specified amount.
        Performs validations to ensure spending operations are legal
        """
        if amount < 0:
            raise NegativeValueError(amount)
        self._validate_operations(token_type)
        if (
            self.__focus_tokens[token_type] < amount
        ):  # validation to see if enough token amount is available to spend
            raise ValueError(f"Not enough {token_type} to spend")
        self.__focus_tokens[token_type] -= amount

    def get_token_count(self, token_type: str) -> int:
        """
        returns the count of a token inside the mutable mapping.
        """
        if token_type not in self.__focus_tokens:
            raise KeyError(f"Token type '{token_type}' not found")
        return self.__focus_tokens[token_type]

    def reset_tokens(self) -> None:
        """
        reset the token count back to zero
        """
        for token in self.__focus_tokens:
            self.__focus_tokens[token] = 0

    @property
    def focus_tokens(self) -> MutableMapping[str, int]:
        return self.__focus_tokens


class InvestigatorItems:
    """
    :cls:`InvestigatorItems` is a collection of resources available to the investigator in the game of Arkham Horror. This class also includes instances of other classes to handle: items, skills, spells, and other resources associated with an investigator interanally. :cls:`InvestigatorItems`, additionally, provides methods for managing these resources.
    """

    _items: List[Item]
    _parent_cls: BaseInvestigator
    _money: int
    __skill: Dict[SkillName, Skill]
    _spells: List[Spell]
    _focus_tokens: MutableMapping[str, int]
    _event_deck: EventDeck
    _encounter_deck: EncounterDeck
    _inv_token: InvestigatorTokens
    _monster_deck: MonsterDeck

    def __new__(
        cls,
        parent_cls: BaseInvestigator,
        event_deck: EventDeck,
        encounter_deck: EncounterDeck,
        inv_tokens: InvestigatorTokens,
        monster_Deck: MonsterDeck,
    ) -> Self:
        """
        The constructor :meth:`__new__` that creates a new instances and intializes it with a set of attributes. It then returns the freshly created and initialized instance.
        """
        self = super().__new__(cls)
        self._parent_cls = parent_cls
        self._focus_tokens = inv_tokens.focus_tokens
        self._items = []
        self._money = 0
        self.__skill = {}
        self._spells = []
        self._event_deck = event_deck
        self._encounter_deck = encounter_deck
        self._monster_deck = monster_Deck
        return self

    def add_item(self, item: Item) -> Self:
        """
        Adds an item to the investigator's list of items.
        part of the Builder pattern implementing a fluent API.
        Returns:
            Self: The instance of the InvestigatorItems class.
        """

        if item in self._items:
            item.amount += 1  # as item exits => increase its amount property
        else:
            self._items.append(item)
        return self

    def add_skill(self, skill: Skill) -> Self:
        """
        Adds a new skill to the investigator's collection of skills.
        part of the Builder pattern implementing a fluent API.

        Returns:
            Self: The instance of the InvestigatorItems class.
        """
        if skill.name in self.__skill:
            raise KeyError(
                "the skill exists already. Cannot add duplicate entries to dictionary"
            )
        else:
            self.__skill[skill.name] = skill
        return self

    def add_spell(self, spell: Spell) -> Self:
        """
        Adds a spell to the collection of investigator's spells.
        part of the Builder pattern implementing a fluent API.

        Returns:
            Self: The instance of the InvestigatorItems class.
        """
        self._spells.append(spell)
        return self

    def add_money(self, amount: int) -> Self:
        """
        Adds money to the collection of investigator's collection.
        Increases money by specified amount.
        Increases the 'money_tokens' in the focus tokens by the same amount.
        Part of the Builder pattern implementing a fluent API.

        Returns:
            Self: The instance of the InvestigatorItems class.

        """
        if amount < 0:
            raise NegativeValueError(amount)

        self._money += amount
        self._focus_tokens["money_tokens"] += amount

        return self

    def spend_money(self, amount: int) -> None:
        """
        Spends a specified amount of money tokens.
        Checks validation to ensure money_token exists in the focus_tokens
        Checks further validation to see that the amount value of 'money_tokens' isn't zero. Also, checks validation to ensure that value to spend isn't negative.

        If all validation passes -> the specified amount is deducted from the 'money_tokens'.
        """
        if "money_tokens" not in self._focus_tokens:
            raise KeyError("key 'money_tokens' not found")

        money_tokens = self._focus_tokens.get("money_tokens")
        # Validation to check that current value of money tokens is not None or negative
        if money_tokens is None:
            raise ValueError("money_tokens is None")

        if value := self._focus_tokens.get("money_tokens") == 0:
            raise ValueError("no money left to spend")

        if value < 0:
            raise NegativeValueError(value)
        # is there enough money to cover the amount needed to spend?
        if money_tokens < amount:
            raise ValueError(
                f"Not enough money tokens to spend. Available: {money_tokens}, Required: {amount}"
            )

        self._focus_tokens[
            "money_tokens"
        ] -= amount  # validation passes, spend the money

    @property
    def items(self) -> List[Item]:
        return self._items

    @property
    def spells(self) -> List[Spell]:
        return self._spells

    @property
    def money(self) -> int:
        return self._money

    @money.setter
    def money(self, money: int) -> None:
        self._money -= money

    @property
    def monster_deck(self) -> MonsterDeck:
        return self._monster_deck

    @property
    def skills(self) -> Dict[SkillName, Skill]:
        return self.__skill

    @property
    def encounter_deck(self) -> EncounterDeck:
        return self._encounter_deck

    @property
    def event_deck(self) -> EventDeck:
        return self._event_deck


class Combat:
    """
    :cls:`Combat`defines methods and attributes needed for the fight between the invetstigator and the monster(s) in the game. It includes instances of other classes (using Composition) to have access to their methods and to delegate operations to them, such as attacking monsters, warding off doom, and evading monsters.
    """

    _inv_items: InvestigatorItems
    _status: InvestigatorStatus
    _parent_cls: BaseInvestigator
    _location: Space
    __engaged_monsters: List[Monster]

    def __init__(
        self,
        investigator: Investigator,
        inventory: Item,
        parent_cls: BaseInvestigator,
    ):
        """
        instantiates an instance of the Combat class
        """

        self._investigator = investigator
        self._inventory = inventory
        self._location = parent_cls.location  # using BaseInvestigator
        self.__engaged_monsters = []

    @property
    def engaged_monsters(self) -> List[Monster]:
        return self.__engaged_monsters

    def ward_doom(self) -> None:
        """
        This method performs a Ward action to remove doom tokens for the location the investigator is at. According to game rules, investigator rolls a number of dice equal to their lore skill level.
        """
        lore_skill: Optional[Skill] = self._inv_items.skills.get(
            SkillName.LORE
        )  # retrieve the lore_skill
        if lore_skill is None:
            raise KeyError("Lore skill not found")

        lev = lore_skill.level(SkillName.LORE)  # get the lore skill level
        if lev is None:
            raise ValueError("Lore skill level is None")
        # each roll resulting in a 5 or more (6) is considered a success.
        num_successes = sum(random.randint(1, 6) >= 5 for _ in range(lev))

        # the number of successes determines how many dooms are removed from the
        # location investigator is at, if smaller than the number of
        # doom tokens. If number of successes is higher, all doom tokens are removed.

        removed_dooms = min(num_successes, self._location.doom_tokens)
        # this number of dooms is removed from the location
        self._location.doom_tokens -= removed_dooms

    def attack_monster(self, monster: Monster) -> None:
        """
        Attacks the given monster and reduces its health by 1.
        """
        if monster not in self.__engaged_monsters:
            raise ValueError("Monster must be engaged to be attacked")
        monster._monster_health.health -= 1

    def evade_monster(self, monster: Monster) -> None:
        """
        Implements logic for investigator to evade a monster they are engaged with. The logic is performed via rolling a number of dice. The number of rolls equals investigator's Observation skill level and is modified by the monster's evade modifier.
        """
        if monster not in self.__engaged_monsters:
            raise ValueError(
                f"investigator {self._investigator} is not engaged with monster {monster}."
            )
        # get observation skill of the investigator
        obs_s: Optional[Skill] = self._investigator._inv_items.skills.get(
            SkillName.OBSERVATION
        )
        if obs_s is None:
            raise KeyError("Observation skill not found")
        # get the level of investigator's observation skill
        obl = obs_s.level
        if obl is None:
            raise ValueError("Observation skill level is None")
        if not isinstance(obl, int):
            raise AttributeError(
                f"observation level isnt an integer. It is: {obl} = "
            )
        # Calculate the number of dice to roll,
        # considering the monster's evade modifier
        num_rolls = max(obl + monster.evade_modifier(), 1)

        # roll the die and sum up the number of successes (5 or higher)
        num_succ = sum(random.randint(1, 6) >= 5 for _ in range(num_rolls))
        # If the number of successful rolls (5 or higher) is greater than 0,
        # the monster is evaded. Evaded monsters become exhausted.
        if num_succ > 0:
            # exhausted monsters get removed from the enaged_monsters
            self._investigator.engaged_monsters.remove(monster)
            # and their state change to exhaustd
            monster._monster_state.exhaust()
        else:
            # if no successes achieved, investigator cannot evade
            # and need to attack the monster
            self.attack_monster(monster)


class InvestigatorSpells:
    """
    :cls:`InvestigatorSpells`Handles an investigator's spell casting abilities and their effects in Arkham Horror Game.
    """

    _combat: Combat
    _status: InvestigatorStatus

    def __init__(self, combat: Combat, status: InvestigatorStatus) -> None:
        self._combat = combat
        self._status = status

    def cast_spell(self, spell: Spell, monster: Monster) -> None:
        """
        Casts a spell on a monster and loses sanity as a consequence.
        """
        if self._status.is_defeated:
            raise AttributeError(
                f"the investigator is defeated and cant perform {spell} action"
            )
        self._combat.attack_monster(monster)  # delegate to Combat
        self._status.lose_sanity(spell.horror)  # delegate to InvestigatorStatus

    def assign_damage(self, damage: int) -> None:
        """
        Reduces the investigator's health by a specified amount.
        """
        if damage < 0:
            raise NegativeValueError(damage)

        self._status.take_damage(damage)  # delegate to InvestigatorStatus

    def assign_horror(self, horror: int) -> None:
        """
        Increase investigator's horror by a specified amount
        """
        if horror <= 0:
            raise NegativeValueError(horror)
        self._status.lose_sanity(horror)  # delegate to InvestigatorStatus


class AbstractMove(ABC):
    """
    An Abtract class designed for move. It defines the blueprint for move method that must be implemented by subclasses
    """

    @abstractmethod
    def move(self, investigator: Investigator, new_space: Space) -> None: ...


class Move(AbstractMove):
    """
    Inherits from :cls:`AbstractMove`. Implements two methods :meth:`calc_distance` which is used by :meth:`move`
    """

    _investigator: Investigator

    def __init__(self, investigator: Investigator) -> None:
        self._investigator = investigator

    def calc_distance(self, start: Space, end: Space) -> int:
        """
        Calculates the Euclidean distance between two locations (Spaces).
        """
        diff_x_axis: float = start._position[0] - end._position[0]
        diff_y_axis: float = start._position[1] - end._position[1]
        distance = int(math.sqrt(diff_x_axis**2 + diff_y_axis**2))
        return distance

    def move(self, investigator: Investigator, new_space: Space) -> None:
        """
        Moves the investigator to a new space up to a maximum of 2 units. If the distance to the new space is more than 2 units, money needs to be spent, according to game rules.
        """

        distance = self.calc_distance(investigator.location, new_space)
        if distance > 4:  # Cannot move beyond 4 units
            raise ValueError(
                "Maximum distance is 2 extra distances an investigator is allowed to spend money on in order to move."
            )
        if distance <= 2:
            # no need to spend money here
            investigator._location = new_space
        else:
            # spend money to move up to two units
            additional_cost: int = distance - 2
            investigator.spend_money(additional_cost)
            # if investigator has money to spend, move to the new location
            investigator._location = new_space


class EncounterResolution:
    """
    :cls:`EncounterResolution`handles resolving encounters for an investigator in the Arkham Horror game.
    """

    _investigator: Investigator

    def resolve_encounter(self) -> None:
        """
        If investigator isnt engaged with monsters, an encounter card is drawn from the encounter deck and resolution is attempted.
        """
        if self._investigator.engaged_monsters:
            raise ValueError(
                "engaged investigators currently engaged with monsters cannot resolve encounters"
            )
        encounter_card = (
            self._investigator._inv_items.encounter_deck.draw_front()
        )
        if encounter_card is None:
            raise ValueError("no encounter card found")

        outcome = encounter_card.resolve_encounter(
            self._investigator
        )  # delegates to EncounterCard


class InvCommand(ABC):
    """
    Abstract Base Class that defines a blueprint for :meth:`execute_action` that subclasses must implement.
    """

    @abstractmethod
    def execute_action(self) -> None: ...


class MoveCommand(InvCommand):
    """
    subclass of :cls:`InvCommand` that represents a command to move an investigator to a new space. It inherits from the ABC InvCommand and uses composition, having an `Investigator` object and to a `Space` object internally
    """

    _invectigator: Investigator
    _new_space: Space

    def __init__(self, investigator: Investigator, new_space: Space) -> None:
        """
        Initializes a new MoveCommand object with specified Investigator and Space.
        """

        self._investigator = investigator
        self._new_space = new_space

    def execute_action(self) -> None:
        """
        When the command is executed, the investigator is moved to the new space.
        """
        self._investigator.move(self._new_space)  # delegates to Investigator


class AttackMonsterCommand(InvCommand):
    """
    subclass of :cls:`InvCommand` that represents a command to attack a monster. It inherits from the ABC InvCommand and uses composition and includes Investigator, Monster and Combat internally.
    """

    _monster: Monster
    _investigator: Investigator
    _combat: Combat

    def __init__(self, investigator: Investigator, monster: Monster) -> None:
        """
        Initializes a new instance of :cls:`AttackMonsterCommand` class with specified Investigator and Monster.
        """
        self._investigator = investigator
        self._monster = monster

    def execute_action(self) -> None:
        """
        When the command is executed, the investigator attacks the monster.
        """
        self._combat.attack_monster(self._monster)  # delegates to Combat


class CastSpellCommand(InvCommand):
    """
    subclass of :cls:`InvCommand` that represents a command to cast spell on a monster. It inherits from the ABC InvCommand and uses composition by including Investigator, Monster and Spell internally.
    """

    _spell: Spell
    _investigator: Investigator
    _monster: Monster

    def __init__(
        self, spell: Spell, investigator: Investigator, monster: Monster
    ) -> None:
        self._investigator = investigator
        self._monster = monster
        self._spell = spell

    def execute_action(self) -> None:
        """
        Upon command execution, the investigator casts spell on the monster.
        """
        self._investigator.cast_spell(self._spell, self._monster)


class WardDoomCommand(InvCommand):
    """
    subclass of :cls:`InvCommand` that represents a command to Ward Doom. It inherits from the ABC InvCommand and uses composition and includes reference to Investigator.
    """

    _investigator: Investigator

    def __init__(self, investigator: Investigator) -> None:
        self._investigator = investigator

    def execute_action(self) -> None:
        """
        execution of command results in call to warding doom logic
        """
        self._investigator.ward_doom()


class Trade:
    """
    This class facicilates trade between an investigator an an ally (also represented as an investigator object for ease of implementation).
    """

    def trade(
        self,
        inv: Investigator,
        ally: Investigator,
        items: List[Item],
        spells: List[Spell],
        money: int,
        clues: List[Clue],
        remnants: int,
    ) -> None:
        """
        Initiates a trade between an investigator and an ally.
        First checks if the two are in the same location through call to :meth:`_validate_trade`
        If the call checks, :meth:`trade` calls :meth:`_perform_trade` to perform the actual trade
        """
        self._validate_trade(inv, ally, items, spells, money, clues, remnants)
        self._perform_trade(inv, ally, items, spells, money, clues, remnants)

    @staticmethod
    def _validate_trade(
        inv: Investigator,
        ally: Investigator,
        items: List[Item],
        spells: List[Spell],
        money: int,
        clues: List[Clue],
        remnants: int,
    ) -> None:
        """Validates trade params."""
        if inv.location != ally.location:
            raise ValueError(
                "Investigators must be in the same location to trade"
            )

    def _perform_trade(
        self,
        inv: Investigator,
        ally: Investigator,
        items: List[Item],
        spells: List[Spell],
        money: int,
        clues: List[Clue],
        remnants: int,
    ) -> None:
        """
        performing trades between an investigator and an ally
        """
        self._trade_items(inv, ally, items)
        self._trade_spells(inv, ally, spells)
        self._trade_money(inv, ally, money)
        self._trade_clues(inv, ally, clues)
        self._trade_remnants(inv, ally, remnants)

    def _trade_items(
        self, inv: Investigator, ally: Investigator, items: List[Item]
    ) -> None:
        """
        Trades items between an investigator and an ally.
        """
        # )a. trading items:
        for item in items:
            # Check if item exists in the inv's item inventory
            if item not in inv._inv_items.items:
                raise NotFoundError(item, inv._inv_items.items)
            else:
                # If found, begin the trade by
                # 1. remove the item from the investigator's inventory
                inv._inv_items.items.remove(item)
                # 2. Add the item to the ally's inventory
                ally._inv_items.add_item(item)

    def _trade_spells(
        self, inv: Investigator, ally: Investigator, spells: List[Spell]
    ) -> None:
        """
        Trades spells between an investigator and an ally.
        """
        # b). trading spells
        for spell in spells:
            # Check if the spell exists in the investigator's spell investory
            if spell not in inv._inv_items.spells:
                raise NotFoundError(spell, inv._inv_items.spells)
            else:
                # If found, begin the trade by
                # 1. remove the spell from the investigator's spell inventory
                inv._inv_items.spells.remove(spell)
                # 2.  Add the spell to the ally's spells
                ally._inv_items.add_spell(spell)

    def _trade_money(
        self, inv: Investigator, ally: Investigator, money: int
    ) -> None:
        """
        Trades money between an investigator and an ally.
        """
        # c. trade money:
        # Check if the inv has enough money to trade
        if money > inv._inv_items.money:
            raise ValueError(
                f"You cannot spend what you don't have. Your money is {inv._inv_items.money} and you are practically broke, mate!"
            )
        if money < 0:
            raise NegativeValueError(money)
        # if enough money is available:
        # 1. remove (deduct) that sum of money from the investigator's account

        inv._inv_items.money -= money
        # 2. Add that sum money to the ally's account
        ally._inv_items.add_money(money)

    def _trade_clues(
        self, inv: Investigator, ally: Investigator, clues: List[Clue]
    ) -> None:
        """
        Trades clues between an investigator and an ally.
        """
        # . d trade clues
        for clue in clues:
            # Check if clue exists in inv's clues
            if clue in inv._inv_clues.clues:
                # 1. remove the clue from inv's clues
                inv._inv_clues.remove_clue(clue)
                # 2. add the clue to the ally's clues
                ally._inv_clues.add_clue(clue)
            else:
                raise NotFoundError(clue, clues)

    def _trade_remnants(
        self, inv: Investigator, ally: Investigator, remnants: int
    ) -> None:
        """
        Trades remnants between an investigator and an ally.
        """
        if inv._invest_token.get_token_count("remnant_tokens") < remnants:
            raise ValueError(f"not enough remnants to spend {remnants}")
        if remnants < 0:
            raise NegativeValueError(remnants)
        # Spend the specified amount of remnant tokens from the investigator
        inv._invest_token.spend_token("remnant_tokens", remnants)
        # Add the specified amount of remnant tokens to the ally
        ally._invest_token.add_token("remnant_tokens", remnants)
