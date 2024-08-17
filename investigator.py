"""
This module contains three classes:
1. Game Data that is a TypedDict representing a database of some sort with attributes common to all investigators
2. A Base Investigator Protocol that defines blueprints for a number of properties. 
3. The Investigator class inherits from Base Investigator and provides a simplified interface, similar to a Facade pattern. It delegates responsibility for more specialized classes. Clients interact with Investigator, which in turn calls methods on internal specialized classes to handle the logic they are good at, thereby simplifying client interaction with the complex underlying system. 
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List, Self, Self, Protocol, TypedDict, Any
from .skills import Skill, SkillName
from .investigator_status import InvestigatorStatus, InvestigatorClues
from .encounter_deck import EncounterDeck
from .event_deck import EventDeck
from .token_pools import TokensInteractions
from .space import Space
from .clue import Clue
from .monster_deck import MonsterDeck
from .item import Item
from .spell import Spell
from .fight_prep import (
        InvestigatorItems,
        Combat,
        Move,
        InvestigatorSpells,
        Trade,
        EncounterResolution,
        InvestigatorTokens,
        MoveCommand,
        AttackMonsterCommand,
        WardDoomCommand,
        CastSpellCommand
    ) 

if TYPE_CHECKING:
    from .monster import Monster
else:
    Monster = Any


class GameData(TypedDict, total=True):
    """
    :cls:`GameData` is a database that holds basic data common to all investigators.
    """

    name: str
    is_lead_investigator: bool
    engaged_monsters: List[Monster]


class BaseInvestigator(Protocol):
    """
    BaseInvestigator is a protocol that defines blueprints for a number of property methods that subclasses need to implement.
    """

    @property
    def name(self) -> str: ...
    @property
    def location(self) -> Space: ...
    @property
    def engaged_monsters(self) -> List[Monster]: ...
    @property
    def status(self) -> InvestigatorStatus: ...


class Investigator(BaseInvestigator):
    """
    Inherits from :cls:`BaseInvestigator` and Represents an investigator in Arkham Horror, providing a simplified interface for interaction with underlying game system.

    :cls:`Investigator` handles various actions, including attacking, moving, casting spells etc. It delegates the actual logic of these actions to specialized internal objects.
    """

    _inv_items: InvestigatorItems
    _inv_clues: InvestigatorClues
    _inv_status: InvestigatorStatus
    _inv_combat: Combat
    _inv_location: Space
    _inv_move: Move
    _inv_spells: InvestigatorSpells
    _inv_trade: Trade
    _game_data: GameData
    _inter_token: TokensInteractions
    _invest_token: InvestigatorTokens
    _inv_encounter: EncounterResolution

    def __new__(
        cls,
        inv_clues: InvestigatorClues,
        inv_items: InvestigatorItems,
        inv_status: InvestigatorStatus,
        inv_location: Space,
        inv_combat: Combat,
        inv_move: Move,
        inv_spells: InvestigatorSpells,
        inv_trade: Trade,
        game_data: GameData,
        inter_token: TokensInteractions,
        inv_encounter: EncounterResolution,
        invest_token: InvestigatorTokens,
    ) -> Self:
        """
        Creates a new instance of the Investigator class.
        """
        self = super().__new__(cls)

        self._inv_clues = inv_clues
        self._inv_items = inv_items
        self._inv_status = inv_status
        self._inv_location = inv_location
        self._inv_combat = inv_combat
        self._inv_move = inv_move
        self._inv_spells = inv_spells
        self._inv_trade = inv_trade
        self._inter_token = inter_token
        self._invest_token = invest_token
        self._inv_encounter = inv_encounter
        return self

    def move(self, space: Space) -> None:
        """
        Moves the investigator to a specified space in the game.
        """
        MoveCommand(self, space).execute_action()

    def attack_monster(self, monster: Monster) -> None:
        """
        Investigator attacks the monster.
        """
        AttackMonsterCommand(self, monster).execute_action()

    def cast_spell(self, spell: Spell, monster: Monster) -> None:
        """
        investigator casts spell on monster
        """
        CastSpellCommand(spell, self, monster).execute_action()

    def ward_doom(self) -> None:
        """
        investigator wards doom
        """
        WardDoomCommand(self).execute_action()

    def evade_monster(self, monster: Monster) -> None:
        """
        investigator attemps to evade monster
        """
        self._inv_combat.evade_monster(monster)

    def add_item(self, item: Item) -> Self:
        """
        add an item to investigators items
        """
        self._inv_items.add_item(item)
        return self

    def spend_money(self, amount: int) -> None:
        """
        investigator attemps to spend some dough
        """
        self._inv_items.spend_money(amount)

    def assign_damage(self, damage: int) -> None:
        """
        Reduces the investigator's health by a specified amount
        """
        self._inv_status.take_damage(damage)

    def assign_horror(self, horror: int) -> None:
        """
        Reduces the investigator's sanity by a specified amount. If amount is negative, raises a NegativeValueError from custom_errors module.
        """
        self._inv_status.lose_sanity(horror)

    def trade(
        self,
        ally: Investigator,
        items: List[Item],
        spells: List[Spell],
        money: int,
        clues: List[Clue],
        remnants: int,
    ) -> None:
        """
        Initiates a trade between an investigator and an ally.
        """
        self._inv_trade.trade(self, ally, items, spells, money, clues, remnants)

    def draw_token(self) -> None:
        """
        Draws tokens from the Mythos Cup during the Mythos Phase
        """
        self._inter_token.draw_token()

    def resolve_encounter(self) -> None:
        """
        investigator attemps to resolve an encounter
        """
        self._inv_encounter.resolve_encounter()

    def draw_event_token(self) -> None:
        """
        Draws an event token from the event deck
        """
        self._inter_token.draw_event_token()

    def draw_monster(self) -> Monster:
        """
        Draws a monster from the monster deck
        """
        return self._inter_token.draw_monster()

    @property
    def engaged_monsters(self) -> List[Monster]:
        return self._inv_combat.engaged_monsters

    @property
    def status(self) -> InvestigatorStatus:
        return self._inv_status.get_status()

    @property
    def monster_deck(self) -> MonsterDeck:
        return self._inv_items.monster_deck

    @property
    def name(self) -> str:
        return self._game_data.get("name", "Unnamed Investigator")

    @property
    def location(self) -> Space:
        return self._location

    @location.setter
    def location(self, new_space: Space) -> None:
        self._location = new_space

    @property
    def event_deck(self) -> EventDeck:
        return self._inv_items.event_deck

    @property
    def encounter_deck(self) -> EncounterDeck:
        return self._inv_items.encounter_deck

    def gather_resources(self) -> None:
        raise NotImplementedError

    def use_item(self, item: Item) -> None: ...

    def research_clues(self) -> None:
        raise NotImplementedError

    def focus(self, skill: SkillName) -> None:
        raise NotImplementedError
