from typing import TYPE_CHECKING, ClassVar, Protocol

if TYPE_CHECKING:
    from ..action_cost import ActionCost
    from ..action_type import ActionType
    from ...creature.character.character import Character
    from ...creature.monster.monster import Monster
    from ...roll.advantage import Advantage

class CharacterAction(Protocol):
    character: "Character"
    name: ClassVar[str]
    description: ClassVar[str]
    cost: ClassVar[list["ActionCost"]]
    action_type: ClassVar["ActionType"]
    advantage: list["Advantage"]
    targets: list["Character|Monster"]

    def execute(self) -> None:
        ...
