from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol
from ..creature.character.berserker import Berserker

if TYPE_CHECKING:
    from ..action.character_action.character_action import CharacterAction
    from ..creature.character.character import Character
    from ..creature.monster.monster import Monster
    from ..encounter.round import Party

from ..logging_setup import get_named_console_logger

logger = get_named_console_logger(__name__)

class Strategy(Protocol):
    character: "Character"
    available_actions: list["CharacterAction"]
    actions_taken: list["CharacterAction"]
    party: "Party"
    enemies: list["Monster"]

    def __str__(self) -> str:
        ...

    def choose_action(self) -> "CharacterAction":
        ...

    def reset(self):
        ...

@dataclass
class AlwaysMeleeAttack:
    character: "Character"
    party: "Party"
    available_actions: list["CharacterAction"] = field(default_factory=list)
    actions_taken: list["CharacterAction"] = field(default_factory=list)
    enemies: list["Monster"] = field(default_factory=list)

    def __str__(self) -> str:
        return "Always Melee Attack"

    def choose_action(self) -> "CharacterAction":
        # get attack action from action
        for action in self.available_actions:
            if action.name == "CharacterAction":
                return action
        return self.available_actions[0]

    def reset(self):
        self.available_actions = []
        self.actions_taken = []


@dataclass
class RageBeforeAttack:
    character: "Character"
    party: "Party"
    available_actions: list["CharacterAction"] = field(default_factory=list)
    actions_taken: list["CharacterAction"] = field(default_factory=list)
    enemies: list["Monster"] = field(default_factory=list)
    rage_threshold: float = 0.5

    def __str__(self) -> str:
        return "Rage before Attack"

    def choose_action(self) -> "CharacterAction":
        # get the attack and rage action from the available actions
        attack = self.get_action_by_name("Attack")
        rage = self.get_action_by_name("Rage")
        
        if attack is None:
            raise Exception("Attack action not found")

        # if character is not a berserker, return the attack action
        if not isinstance(self.character, Berserker):
            logger.debug("Character is not a berserker")
            logger.debug(f"Returning {attack} action")
            return attack

        # if the sum of the fury dice are above the threshold, return the attack action
        max_fury = self.character.max_fury_dice * self.character.fury_die.sides
        total_fury = sum(die.last_roll for die in self.character.fury_dice)
        if total_fury / max_fury >= self.rage_threshold:
            logger.debug(f"Character is raging but above rage threshold, returning {attack} action")
            return attack

        # check if rage action is available and has not already been taken
        if rage not in self.actions_taken and rage is not None:
            logger.debug(f"Returning {rage} action")
            return rage
        
        return attack

    def get_action_by_name(self, name: str) -> "CharacterAction|None":
        for action in self.available_actions:
            if action.name == name:
                return action
        return None

    def reset(self):
        self.available_actions = []
        self.actions_taken = []
