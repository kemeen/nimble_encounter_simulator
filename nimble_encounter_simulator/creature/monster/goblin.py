from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar
from logging import getLogger

from nimble_encounter_simulator.creature.character.character import Character


from ..health import Health
from .monster import Monster, MonsterAncestry, MonsterArmor, MonsterRole

if TYPE_CHECKING:
    from ...encounter.turn import Turn
    from ...action.monster_action.monster_action import MonsterAction
    from ...roll.attack_roll import AttackRoll

logger = getLogger(__name__)

@dataclass
class Goblin:
    monster_ancestry: ClassVar["MonsterAncestry"] = MonsterAncestry.GOBLIN
    role: MonsterRole
    name: str
    description: ClassVar[str] = "A small and agile creature that can be easily killed by a single blow."
    level: int
    health: Health
    armor: MonsterArmor

    @property
    def is_alive(self) -> bool:
        return self.health.wounds < self.health.max_wounds
    
    def __str__(self) -> str:
        return f"{self.name} ({self.monster_ancestry}, {self.level}, {self.role})"
    
    def take_turn(self, turn: "Turn") -> "Turn":
        # TODO
        return turn
    
    def take_damage(self, damage_roll: "AttackRoll") -> None:
        # take full damage if the roll is critical or wearing only light armor
        if self.armor == MonsterArmor.LIGHT or damage_roll.is_last_roll_critical():
            self.health.take_damage(damage_roll.full_damage())
            logger.debug(f"{self} takes {damage_roll.full_damage()} damage")
            return
        # if the armor type is medium only take damage from the rolled dice
        if self.armor == MonsterArmor.MEDIUM:
            damage = sum(die.last_roll for die in damage_roll.last_roll)
            self.health.take_damage(damage)
            logger.debug(f"{self} takes {damage} damage")
            return
        # if the armor type is heavy only take half the damage from the rolled dice
        if self.armor == MonsterArmor.HEAVY:
            damage = sum(die.last_roll for die in damage_roll.last_roll) // 2
            self.health.take_damage(damage)
            logger.debug(f"{self} takes {damage} damage")
            return
        
    def deal_damage(self, damage_roll: "AttackRoll", target: "Monster|Character") -> None:
        if damage_roll.is_last_roll_failed():
            logger.debug(f"{self} misses {target}")
            return
        
        attack_roll = damage_roll.copy()
        logger.debug(f"{self} deals {attack_roll} damage to {target}")
        target.take_damage(attack_roll)
        
def get_melee_goblin(name: str, level: int=1, actions: list["MonsterAction"]=[]):
    return Goblin(
        name=name, 
        level=level, 
        role=MonsterRole.MELEE, 
        health=Health(current_hit_points=10, max_hit_points=10, temporary_hit_points=0, wounds=0, max_wounds=1), 
        armor=MonsterArmor.LIGHT, 
        )

def get_armored_melee_goblin(name: str, level: int=1, actions: list["MonsterAction"]=[]):
    return Goblin(
        name=name, 
        level=level, 
        role=MonsterRole.MELEE, 
        health=Health(current_hit_points=15, max_hit_points=15, temporary_hit_points=0, wounds=0, max_wounds=1), 
        armor=MonsterArmor.MEDIUM, 
        )