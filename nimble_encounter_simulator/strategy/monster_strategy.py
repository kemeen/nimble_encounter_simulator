from dataclasses import dataclass, field
from typing import Protocol

from ..action.monster_action.monster_action import MonsterAction
from ..creature.character.character import Character
from ..creature.monster.monster import Monster

from ..logging_setup import get_named_console_logger

logger = get_named_console_logger(__name__)

class MonsterStrategy(Protocol):
    monster: "Monster"
    available_actions: list["MonsterAction"] = field(default_factory=list)
    actions_taken: list["MonsterAction"] = field(default_factory=list)
    targets: list["Monster|Character"] = field(default_factory=list)

    def __str__(self) -> str:
        ...

    def choose_action(self) -> "MonsterAction":
        ...

    def reset(self):
        ...

@dataclass
class MonsterAlwaysMeleeAttack:
    monster: "Monster"
    available_actions: list["MonsterAction"] = field(default_factory=list)
    actions_taken: list["MonsterAction"] = field(default_factory=list)
    targets: list["Monster|Character"] = field(default_factory=list)

    def __str__(self) -> str:
        return "Monster will always melee attack"

    def choose_action(self) -> "MonsterAction":
        # get attack action from action
        for action in self.available_actions:
            if action.name == "Attack":
                return action
        raise Exception("Attack action not found")

    def reset(self):
        self.available_actions = []
        self.actions_taken = []