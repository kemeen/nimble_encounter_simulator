from dataclasses import dataclass
import random


@dataclass
class Die:
    sides: int = 4
    last_roll: int = 0
    is_primary: bool = False

    def __str__(self) -> str:
        return f"Sides: {self.sides}, Last Roll: {self.last_roll}, Primary: {self.is_primary}"
    
    def roll(self):
        self.last_roll = random.randint(1, self.sides)

    def copy(self):
        return Die(sides=self.sides, last_roll=self.last_roll, is_primary=self.is_primary)
