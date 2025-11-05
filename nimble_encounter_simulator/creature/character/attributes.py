from dataclasses import dataclass
from ...roll.advantage import Advantage

@dataclass
class Attribute:
    value: int
    advantage: Advantage
    is_key: bool

@dataclass
class Attributes:
    strength: Attribute
    dexterity: Attribute
    intelligence: Attribute
    willpower: Attribute

    
    @property
    def max_key(self) -> int:
        return max(self.key_attributes, key=lambda a: a.value).value
    
    @property
    def attributes(self) -> list[Attribute]:
        return [self.strength, self.dexterity, self.intelligence, self.willpower]

    @property
    def key_attributes(self) -> list[Attribute]:
        return [attribute for attribute in self.attributes if attribute.is_key]
        

    
