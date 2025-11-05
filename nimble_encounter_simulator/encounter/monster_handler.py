from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from logging import getLogger

logger = getLogger(__name__)

if TYPE_CHECKING:
    from .turn import Turn
    from ..action.monster_action.monster_action import MonsterAction
    from ..creature.monster.monster import Monster
    from ..strategy.monster_strategy import MonsterStrategy


@dataclass
class MonsterHandler:
    monster: "Monster"
    strategy: "MonsterStrategy"
    actions: list["MonsterAction"] = field(default_factory=list)

    def __str__(self):
        return f"{self.monster.name} ({self.monster.monster_ancestry}, {self.monster.level}, {self.monster.role})"
    
    def register_action(self, action: "MonsterAction"):
        self.actions.append(action)

    def take_turn(self, turn: "Turn"):
        logger.debug(f"Turn for {self.monster}")
        # update the strategy
        self.strategy.targets = [player.creature for player in turn.party.players]
        # use strategy to pick actions
        action = self.strategy.choose_action()
        # execute actions
        

        return turn