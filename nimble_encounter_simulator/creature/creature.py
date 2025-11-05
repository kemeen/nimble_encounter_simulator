from typing import Protocol

from nimble_encounter_simulator.items.weapon.weapon import Weapon
from nimble_encounter_simulator.roll.attack_roll import AttackRoll
from nimble_encounter_simulator.roll.die import Die


class Creature(Protocol):
    name: str
    weapon: "Weapon"

    @property
    def is_alive(self) -> bool:
        ...

    @property
    def attack_dice(self) -> list["Die"]:
        ...

    def get_attack_bonus(self) -> int:
        ...

    def take_damage(self, damage_roll: "AttackRoll"):
        ...

    def deal_damage(self, damage_roll: "AttackRoll", target: "Creature"):
        ...
