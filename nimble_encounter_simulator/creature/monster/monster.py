from enum import StrEnum
from typing import TYPE_CHECKING, ClassVar, Protocol, runtime_checkable

if TYPE_CHECKING:
    from ..health import Health
    from ...encounter.turn import Turn
    from ...roll.attack_roll import AttackRoll
    from ...creature.creature import Creature

class MonsterRole(StrEnum):
    MELEE = "Most effective when toe-to-toe"
    RANGED = "Most effective at Range"
    CONTROLLER = "Hampers the heroes, low damage"
    SUPPORT = "Primarily boosts the damage or abilities of their allies"
    AOE = "Deals damage to multiple heroes at a time (cleaving strikes, shouts, auras, etc.)"
    SUMMONER = "Summons additional monsters to the battlefield (usually minions)"
    STRIKER = "High damage, low survivability"
    AMBUSHER = "Not immediately visible when combat begins"
    DEFENDER = "High survivability, low damage"
    LEGENDARY = "Unique and powerful"

class MonsterArmor(StrEnum):
    LIGHT = "Light armor"
    MEDIUM = "Medium armor"
    HEAVY = "Heavy armor"    

class MonsterAncestry(StrEnum):
    ABERRATION = "Aberration"
    BEAST = "Beast"
    CELESTIAL = "Celestial"
    CONSTRUCT = "Construct"
    DRAGON = "Dragon"
    ELEMENTAL = "Elemental"
    FEY = "Fey"
    GIANT = "Giant"
    HUMANOID = "Humanoid"
    MONSTROSITY = "Monstrosity"
    OOZE = "Ooze"
    PLANT = "Plant"
    UNDEAD = "Undead"
    GOBLIN = "Goblin"
    GNOLL = "Gnoll"

@runtime_checkable
class Monster(Protocol):
    monster_ancestry: ClassVar[MonsterAncestry]
    role: MonsterRole
    name: str
    description: ClassVar[str]
    level: int
    health: "Health"
    armor: MonsterArmor

    @property
    def is_alive(self) -> bool:
        ...
    
    def __str__(self) -> str:
        ...

    def take_turn(self, turn: "Turn") -> "Turn":
        ...

    def take_damage(self, damage_roll: "AttackRoll") -> None:
        ...

    def deal_damage(self, damage_roll: "AttackRoll", target: "Creature") -> None:
        ...