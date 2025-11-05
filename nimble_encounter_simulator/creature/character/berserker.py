from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .character import Character
from ...items.weapon.unarmed import unarmed_attack
from ...effect.feature import Feature
from ...effect.trigger import Trigger
from .character_features import CharacterFeatures
from ...roll.die import Die
from ..health import Health
from .nimble_class import NimbleClass
from ...roll.advantage import Advantage
from .attributes import Attribute, Attributes
from ...logging_setup import get_named_console_logger

logger = get_named_console_logger(__name__)

if TYPE_CHECKING:
    from ..monster.monster import Monster
    from ...roll.attack_roll import AttackRoll
    from ...items.weapon.weapon import Weapon

@dataclass
class Berserker:
    name: str
    attributes: Attributes
    hero_class: NimbleClass
    ancestry: str
    health: Health
    level: int
    weapon: "Weapon" = field(default_factory=unarmed_attack)
    features: CharacterFeatures = field(default_factory=CharacterFeatures)
    fury_die: "Die" = field(default_factory=Die)
    fury_dice: list["Die"] = field(default_factory=list)
    is_raging: bool = False

    def __str__(self) -> str:
        return f"{self.name} ({self.hero_class}) {len(self.fury_dice)} fury dice"

    @property
    def max_fury_dice(self):
        return self.attributes.max_key

    @property
    def attack_dice(self) -> list["Die"]:
        return [die.copy() for die in self.weapon.damage_dice]
        
    def get_attack_bonus(self) -> int:
        # get weapon attack bonus
        return getattr(self.attributes, self.weapon.bonus_stat.value).value
    

    @classmethod
    def new(cls, name: str, strength: int, dexterity: int, intelligence: int, willpower: int, ancestry: str):
        berserker = cls(
            name=name,
            attributes=Attributes(
                strength=Attribute(value=strength, advantage=Advantage.ADVANTAGE, is_key=True),
                dexterity=Attribute(value=dexterity, advantage=Advantage.NEUTRAL, is_key=True),
                intelligence=Attribute(value=intelligence, advantage=Advantage.DISADVANTAGE, is_key=False),
                willpower=Attribute(value=willpower, advantage=Advantage.NEUTRAL, is_key=False),            
            ),
        health=Health(
            current_hit_points=20,
            max_hit_points=20,
            temporary_hit_points=0,
            wounds=0,
            max_wounds=6,
        ),
        hero_class=NimbleClass.BERSERKER,
        ancestry=ancestry,
        level=1,
    )
        return berserker
    
    def register_feature(self, feature: "Feature"):
        feature.character = self
        self.features.register_feature(feature)
    
    def take_damage(self, damage_roll: "AttackRoll") -> None:
        self.health.take_damage(damage_roll.full_damage())

    def deal_damage(self, damage_roll: "AttackRoll", target: "Monster|Character") -> None:
        if damage_roll.is_last_roll_failed():
            logger.debug(f"{self} misses {target}")
            return
        attack_roll = damage_roll.copy()
        attack_roll.last_roll.extend(self.fury_dice.copy())
        logger.debug(f"{self} deals {attack_roll} damage to {target}")
        target.take_damage(attack_roll)

    def on_turn_start(self):
        # get features that trigger on turn start
        logger.debug("on turn start")
        for feature in self.features.features_by_trigger(Trigger.ON_TURN_START):
            logger.debug(feature)
            feature.apply()
            feature.is_active = True

    def on_turn_end(self) -> None:
        pass    