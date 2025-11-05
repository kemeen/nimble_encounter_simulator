from argparse import Action
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol

from ..logging_setup import get_named_console_logger

logger = get_named_console_logger(__name__)

if TYPE_CHECKING:
    from .monster_handler import MonsterHandler
    from ..action.action import Action
    from .party import Party
    from ..creature.creature import Creature


class Actor(Protocol):
    creature: "Creature"
    
    def take_turn(self, turn: "Turn") -> "Turn":
        ...
    

@dataclass
class Turn:
    actor: "Actor"
    party: "Party"
    enemies: list["MonsterHandler"] = field(default_factory=list)
    action_points: int = 3
    actions_taken: list["Action"] = field(default_factory=list)

    @property
    def is_finished(self):
        return self.action_points <= len(self.actions_taken)
    
    def reset(self):
        self.actions_taken = []

    def take_turn(self):
        logger.debug(f"Turn for {self.actor}")
        return self.actor.take_turn(turn=self)