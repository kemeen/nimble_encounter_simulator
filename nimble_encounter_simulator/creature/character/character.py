from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol


from .character_features import CharacterFeatures

if TYPE_CHECKING:
    from ...effect.feature import Feature
    from .attributes import Attributes
    from .nimble_class import NimbleClass
    from ..health import Health
    from ...roll.die import Die
    from ...roll.attack_roll import AttackRoll
    from ..monster.monster import Monster
    from ...items.weapon.weapon import Weapon

@dataclass
class Character(Protocol):
    name: str
    attributes: "Attributes"
    hero_class: "NimbleClass"
    ancestry: str
    health: "Health"
    level: int
    weapon: "Weapon"
    features: CharacterFeatures = field(default_factory=CharacterFeatures)
    
    
    @property
    def attack_dice(self) -> list["Die"]:
        ...

    def get_attack_bonus(self) -> int:
        ...

    def register_feature(self, feature: Feature) -> None:
        ...

    def on_turn_start(self) -> None:
        ...

    def on_turn_end(self) -> None:
        ...

    def take_damage(self, damage_roll: "AttackRoll") -> None:
        ...

    def deal_damage(self, damage_roll: "AttackRoll", target: "Monster|Character") -> None:
        ...