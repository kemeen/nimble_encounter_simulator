from enum import Enum, auto
from typing import Protocol

class ItemTier(Enum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EPIC = auto()
    LEGENDARY = auto()


class Item(Protocol):
    name: str
    description: str
    value: int
    size: int
    stack_size: int
    tier: ItemTier