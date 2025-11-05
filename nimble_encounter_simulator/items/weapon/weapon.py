from dataclasses import dataclass
from enum import StrEnum

from ...roll.die import Die
from ..item import ItemTier

class WeaponBonusStat(StrEnum):
    STR = "strength"
    DEX = "dexterity"
    INT = "intelligence"
    WIL = "willpower"

class DamageType(StrEnum):
    PIERCING = "piercing"
    SLASHING = "slashing"
    BLUDGE = "bludgeoning"

@dataclass
class WeaponProperties:
    two_handed: bool
    load: bool
    reach: int
    range: int
    thrown: bool
    vicious: bool
    light: bool

@dataclass
class Weapon:
    name: str
    description: str
    value: int
    size: int
    stack_size: int
    tier: ItemTier
    properties: WeaponProperties
    damage_dice: list["Die"]
    bonus_stat: WeaponBonusStat
    damage_types: list[DamageType]
    requirements: list[tuple[WeaponBonusStat, int]]
