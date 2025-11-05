from dataclasses import dataclass, field
from typing import ClassVar

from ..action_type import ActionType
from ...creature.character.character import Character
from ...creature.monster.monster import Monster
from ...roll.advantage import Advantage
from ..action_cost import ActionCost
from ..action_ressource import ActionRessource
from ...roll.attack_roll import AttackRoll
from ...logging_setup import get_named_console_logger

logger = get_named_console_logger(__name__)

@dataclass
class MonsterAttack:
    monster: "Monster" 
    damage_roll: "AttackRoll" 
    name: ClassVar[str] = "Attack"
    description: ClassVar[str] = "Attack the target"
    cost: ClassVar[list[ActionCost]] = [ActionCost(amount=1, ressource=ActionRessource.ACTION_POINT)]
    action_type: ClassVar[ActionType] = ActionType.ATTACK
    advantage: list["Advantage"] = field(default_factory=list)
    targets: list["Character|Monster"] = field(default_factory=list)
    attack_range: tuple[int, int] = (1,1)

    def __str__(self):
        return f"{self.name} ({self.description})"
    
    def execute(self):
        # roll for attack against each of the targets
        logger.debug(f"{self.monster.name} attacks {len(self.targets)} targets with the {self.name} action for {self.damage_roll.dice} dice")
        self.damage_roll.roll()
        if self.damage_roll.is_last_roll_failed():
            logger.debug(f"{self.monster.name} misses its attack!")
            return

        for target in self.targets:
            self.monster.deal_damage(damage_roll=self.damage_roll, target=target)
            #print(f"{creature} attacks {target} for {roll.full_damage()} damage")
