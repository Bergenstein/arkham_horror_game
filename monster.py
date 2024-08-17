"""
This module defines the Monster class and associated methods required to managing states and behaviors of monsters in Arkham Horror. It handles logic for engagement between Monster and Investigators (another core component of the game), taking damage, etc. It also handles the state transition of monsters between their allowed states in the game rules: ready, engaged,  exhausted. It has three classes: 
1. BaseMonster(Protocol): defines a set of blueprints for subclasses to follow
2. ReadyMonster(Protocol): Interface for monsters in the ready state.
3. EngagedMonster(Protocol): Interface for monsters in the engaged state.
4. ExhaustedMonster(Protocol): Interface for monsters in the exhausted state.
5. Monster: Concrete monster class that handles state transitions.
6. MonsterState: class managing state transitions of a monster.
7. MonsterHealth: class managing health related activities.
8. MonsterEngagement: class Managing monster engagement with its prey(investigator).
9. MonsterActivation: class Managing monster activation; uses builder pattern.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Protocol, Optional, Self, cast, Any
from .custom_errors import NegativeValueError
from .space import Space

if TYPE_CHECKING:
    from .investigator import Investigator
else:
    Investigator = Any


# possible states of a monster.
MonsterStages = Literal["ready", "exhausted", "engaged"]


class BaseMonster(Protocol):
    """
    This interface :cls:`BaseMonster` defines blueprint for properties and methods common to all monsters.
    """

    @property
    def name(self) -> str: ...

    @property
    def health(self) -> int: ...

    def take_damage(self, amount: int) -> None: ...

    def attack(self) -> int: ...

    def is_defeated(self) -> bool: ...


# Define protocols for each state of the monster.
class ReadyMonster(BaseMonster, Protocol):
    """
    Interface for monsters in the ready state.
    """

    @property
    def state(self) -> Literal["ready"]: ...

    def engage(self, investigator: Investigator) -> EngagedMonster: ...


class EngagedMonster(BaseMonster, Protocol):
    """
    Interface for monsters in the engaged state.
    """

    @property
    def state(self) -> Literal["engaged"]: ...

    def attack(self) -> int: ...

    def exhaust(self) -> ExhaustedMonster: ...

    def disengage(self) -> ReadyMonster: ...


class ExhaustedMonster(BaseMonster, Protocol):
    """
    Interface for monsters in the exhausted state.
    """

    @property
    def state(self) -> Literal["exhausted"]: ...

    def ready(self) -> ReadyMonster: ...


class Monster:
    """
    A concrete implementation of a Monster that can transition between different states.
    """

    _name: str
    _damage: int
    _monster_health: MonsterHealth
    _monster_engagement: MonsterEngagement
    _monster_activation: MonsterActivation
    _monster_state: MonsterState

    def __new__(
        cls,
        name: str,
        damage: int,
        health: int,
        monster_engagement: MonsterEngagement,
        monster_activation: MonsterActivation,
    ) -> Monster:
        """
        The constructor :meth:`__new__`for a concrete monster :cls:`Monster` that initializes a new instance of the Monster class and sets its attributes. It then returns an instance of the Monster class in the ready state.
        """
        self = super().__new__(cls)
        self._name = name
        self._damage = damage
        self._monster_health = MonsterHealth(health, MonsterState("ready"))
        self._monster_engagement = monster_engagement
        self._monster_activation = monster_activation
        return self

    def as_ready_monster(self) -> ReadyMonster:
        """
        Cast the current instance to a ReadyMonster.
        This is just for type hinting; the actual instance remains the same.
        """
        return cast(ReadyMonster, self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def health(self) -> int:
        return self._monster_health.health

    @property
    def state(self) -> MonsterStages:
        return self._monster_health._state.stage

    def take_damage(self, amount: int) -> None:
        """
        Applies damage to the monster by a specified amount.
        """
        self._monster_health.get_damaged(amount)  # delegates to MonsterHealth

    def attack(self) -> int:
        """
        monster launching an attack on an investigator
        """
        if self.state != "engaged":
            raise AttributeError(
                f"Monster cannot attack in stage {self.state}."
            )
        return self._damage

    def is_defeated(self) -> bool:
        """
        checks if monster is defeated
        """
        return (
            not self._monster_health.check_health_status()
        )  # delegates to MonsterHealth

    def engage(self, investigator: Investigator) -> EngagedMonster:
        """
        Method defining logic to engage the monster with an investigator. It returns the Monster in its Engaged state.
        """
        if self.state != "ready":
            raise AttributeError(
                f"Monster can only engage in the 'ready' state. The state is {self.state}"
            )
        self._monster_engagement.start_engagement(
            investigator
        )  # delegates to MonsterEngagement
        self._monster_health._state.engage()  # delegates to MonsterHealth
        return cast(EngagedMonster, self)

    def exhaust(self) -> ExhaustedMonster:
        """
        Method defining logic to exhaust the monster. It returns the Monster in its Exhausted state.
        """
        if self.state != "engaged":
            raise AttributeError(
                f"Monster can only be exhausted in the 'engaged' state. The current state is {self.state}"
            )
        self._monster_health._state.exhaust()  # delegates to MonsterState
        return cast(ExhaustedMonster, self)

    def disengage(self) -> ReadyMonster:
        """
        Method defining logic to disengage the monster. It returns the Monster in its Disengaged state.
        """
        if self.state != "engaged":
            raise AttributeError(
                f"Monster can only disengage in the 'engaged' state. The current state is {self.state}"
            )
        # no more fighting at this point
        self._monster_engagement.no_fight()  # delegates to MonsterEngagement
        self._monster_health._state.ready()  # delegats to MonsterState
        return cast(ReadyMonster, self)

    def ready(self) -> ReadyMonster:
        """
        Method defining logic to ready the monster. It returns the Monster in its Ready state.
        """
        if self.state != "exhausted":
            raise AttributeError(
                f"Monster can only be readied from the 'exhausted' state. The current state is {self.state}"
            )
        self._monster_health._state.ready()  # delegats to MonsterState
        return cast(ReadyMonster, self)

    def set_location(self, location: Space) -> Self:
        """
        Sets the location (Space) of the monster and returns monster instance with its updated location.
        """
        self._monster_activation.set_location(
            location
        )  # delegates to MonsterActivation
        return self

    def evade_modifier(self) -> int:
        """
        Method to retrieve the evade modifier of a monster.
        """
        return (
            self._monster_activation.evade_modifier
        )  # delegates to MonsterActivation

    def __repr__(self) -> str:
        """
        dunder method implementing pretty string representation of Monster instance.
        """
        return f"Monster(name={self.name}, health={self.health}, damage={self._damage}, stage={self.state}, speed={self._monster_activation.speed})"


class MonsterState:
    """
    class handling state transition for a monster inside of the Arkham Horror Game
    """

    _stage: MonsterStages

    def __init__(self, stage: MonsterStages) -> None:
        self._stage = stage

    @property
    def stage(self) -> MonsterStages:
        return self._stage

    def engage(self) -> None:
        """
        sets the Monster stage to engaged
        """
        self._stage = "engaged"

    def exhaust(self) -> None:
        """
        Sets the Monster stage to exhausted.
        Returns None, so it should not be used in a boolean context.
        """
        self._stage = "exhausted"

    def ready(self) -> None:
        """
        sets the Monster stage to ready
        """
        self._stage = "ready"


class MonsterHealth:
    """
    class managing monster health and some routines to handle activities that affect its health such as taking damage as well as methods for health validation and interactions with MonsterState as it composes an instance of MonsterState internally.
    """

    __health: int
    _state: MonsterState

    def __init__(self, health: int, state: MonsterState) -> None:
        self.__set_health(health)
        self._state = state

    @classmethod
    def _validate_health(cls, health: int) -> int:
        """
        Health validation mechanism. Raises a custom NegativeValueError if health is negative.
        """
        if health < 0:
            raise NegativeValueError(health)
        return health

    def __set_health(self, health: int) -> None:
        """
        Private method that sets the __health attribute.
        First performs health validation
        """
        self.__health = type(self)._validate_health(
            health
        )  # delegated validation to `_validate_health`

    def get_damaged(self, amount: int) -> None:
        """
        Applies damage to a monster by a specified amount. It performs validations to prevent illegal actions.
        """
        if amount < 0:
            raise NegativeValueError(amount)
        if self.health <= 0:
            raise AttributeError("Monster has already been defeated")
        if self._state.stage == "exhausted":
            self.__health -= amount * 2  # exhausted monsters get more damage
        else:
            self.__health -= amount
        if self.__health < 0:
            self.__health = 0

    def check_health_status(self) -> bool:
        """
        checks monster's health status to see if still alive
        """
        return self.__health > 0

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, val: int) -> None:
        """
        Setter for health attribute of :class:`MonsterHealth`.
        """
        self.__set_health(val)


class MonsterEngagement:
    """
    class that handles engagement of the Monster with its prey. A monster can have one or no prey. A monster cannot be engaged with more than one prey according to game rules. The class has methods to support operations that handles engagement related activities.
    """

    _prey: Optional[Investigator]
    _state: MonsterState

    def __init__(
        self, state: MonsterState, prey: Optional[Investigator] = None
    ):
        """
        :meth:`__init__`initializes a new instance of :class:`MonsterEngagement` with an optional :class:`Investigator` as prey and a :class:`MonsterState`.
        """
        self._prey = prey
        self._state = state

    def start_engagement(self, investigator: Investigator) -> None:
        """
        To start the engagement, the monster's prey is set to a specified investigator.
        """

        if self._state.stage != "ready":
            raise AttributeError(
                f"Already engaged or exhausted monsters cannot engage investigators. The state is {self._state.stage}"
            )
        self._prey = investigator

    def no_fight(self) -> None:
        """
        Disengages the monster from its current prey by simply removing the prey from the monster
        """

        if self._state.stage != "engaged":
            raise AttributeError("Monster must be engaged to disengage.")
        self._prey = None

    @property
    def prey(self) -> Optional[Investigator]:
        return self._prey


class MonsterActivation:
    """
    class managing monster Activation. This class utilizes Builder Pattern to implement a fluent API
    """

    _speed: int
    _name: str
    _evade_modifier: int
    _location: Space

    def __init__(
        self, speed: int, name: str, modifier: int, location: Space
    ) -> None:
        """
        Initializes a new instance of :class:`MonsterActivation` with the monster's speed, name, evade modifier, and location.
        """
        self._speed = speed
        self._name = name
        self._evade_modifier = modifier
        self._location = location

    def set_speed(self, speed: int) -> Self:
        """
        sets speed of monster
        part of builder pattern for :cls:`MonsterActivation`
        returns self to implement the fluent API
        """
        self._speed = speed
        return self

    def set_activation_text(self, text: str) -> Self:
        """
        sets activation_text attribute of monster
        part of builder pattern for :cls:`MonsterActivation`
        returns self to implement the fluent API
        """
        self._activation_text = text
        return self

    def set_name(self, name: str) -> Self:
        """
        sets name attribute of monster
        part of builder pattern for :cls:`MonsterActivation`
        returns self to implement the fluent API
        """
        self._name = name
        return self

    def set_spawn_text(self, text: str) -> Self:
        """
        sets spawn_text attribute of monster
        part of builder pattern for :cls:`MonsterActivation`
        returns self to implement the fluent API
        """
        self._spawn_text = text
        return self

    def set_modifier(self, modifier: int) -> Self:
        """
        sets evade_modifier attribute of monster
        part of builder pattern for :cls:`MonsterActivation`
        returns self to implement the fluent API
        """
        self._evade_modifier = modifier
        return self

    def set_location(self, loc: Space) -> Self:
        """
        sets location attribute of monster
        part of builder pattern for :cls:`MonsterActivation`
        returns self to implement the fluent API
        """
        self._location = loc
        return self

    @property
    def evade_modifier(self) -> int:
        return self._evade_modifier

    @property
    def name(self) -> str:
        return self._name

    @property
    def speed(self) -> int:
        return self._speed
