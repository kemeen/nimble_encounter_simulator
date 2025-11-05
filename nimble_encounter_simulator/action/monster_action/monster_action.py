from typing import TYPE_CHECKING, ClassVar, Protocol

if TYPE_CHECKING:
    from ..action_cost import ActionCost
    from ...creature.character.character import Character
    from ...creature.monster.monster import Monster
    from ...roll.advantage import Advantage
    from ..action_type import ActionType
    from ...roll.attack_roll import AttackRoll


class MonsterAction(Protocol):
    monster: "Monster"
    damage_roll: "AttackRoll" 
    name: ClassVar[str]
    description: ClassVar[str]
    action_type: ClassVar["ActionType"]
    cost: ClassVar[list["ActionCost"]]
    advantage: list["Advantage"]
    targets: list["Character|Monster"]
    attack_range: tuple[int, int]

    def execute(self) -> None:
        ...