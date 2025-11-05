# A feature is a characteristic of a character that have a trigger.
# The difference to an action is that it is not ab active choice by the player but happens without confirmation.
# It can be added to a character at any time. It might also trigger once when added and never again.

from typing import TYPE_CHECKING, ClassVar, Protocol


if TYPE_CHECKING:
    from ..creature.character.character import Character
    from .trigger import Trigger

class Feature(Protocol):
    name: ClassVar[str]
    description: ClassVar[str]
    trigger: "Trigger"
    is_active: bool
    character: "Character"

    def __str__(self):
        return f"{self.name}: {self.description}"

    def apply(self):
        ...

