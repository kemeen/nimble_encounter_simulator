from dataclasses import dataclass, field
from typing import ClassVar

from .character_action import ActionType
from ...creature.character.character import Character
from ...creature.monster.monster import Monster
from ...roll.advantage import Advantage
from ..action_cost import ActionCost
from ..action_ressource import ActionRessource
from ...roll.attack_roll import AttackRoll
from ...logging_setup import get_named_console_logger

logger = get_named_console_logger(__name__)

@dataclass
class MeleeAttack:
    character: "Character" 
    name: ClassVar[str] = "Attack"
    description: ClassVar[str] = "Attack the target"
    cost: ClassVar[list[ActionCost]] = [ActionCost(amount=1, ressource=ActionRessource.ACTION_POINT)]
    action_type: ClassVar[ActionType] = ActionType.ATTACK
    advantage: list["Advantage"] = field(default_factory=list)
    targets: list["Character|Monster"] = field(default_factory=list)

    def __str__(self):
        return f"{self.name} ({self.description})"
    
    def execute(self):
        # roll for attack against each of the targets
        logger.debug(f"{self.character.name} attacks {len(self.targets)} targets with {self.character.weapon.name} for {self.character.weapon.damage_dice} dice")
        roll = AttackRoll(dice=self.character.attack_dice, bonus=self.character.get_attack_bonus(), advantage=self.advantage)
        roll.roll()

        for target in self.targets:
            self.character.deal_damage(damage_roll=roll, target=target)
            #print(f"{creature} attacks {target} for {roll.full_damage()} damage")
