from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from ..logging_setup import get_named_console_logger

from .advantage import Advantage

if TYPE_CHECKING:
    from .die import Die

logger = get_named_console_logger(__name__)


@dataclass
class AttackRoll:
    dice: list["Die"]
    bonus: int
    advantage: list[Advantage] = field(default_factory=list)
    last_roll: list["Die"] = field(default_factory=list)

    def __str__(self) -> str:
        if len(self.last_roll) == 0:
            return "NOT ROLLED YET!"

        return f"[{', '.join(str(die) for die in self.last_roll)}] + {self.bonus} + {' '.join(str(adv) for adv in self.advantage)}"

    def copy(self):
        return AttackRoll(dice=self.dice.copy(), bonus=self.bonus, advantage=self.advantage.copy(), last_roll=self.last_roll.copy())

    def is_last_roll_failed(self):
        return self.last_roll_primary_die().last_roll == 1
    
    def is_last_roll_critical(self):
        return self.last_roll_primary_die().last_roll == self.last_roll_primary_die().sides

    def add_advantage(self, amount: int):
        self.advantage.extend([Advantage.ADVANTAGE] * amount)

    def add_disadvantage(self, amount: int):
        self.advantage.extend([Advantage.DISADVANTAGE] * amount)

    def total_advantage(self):
        return sum(self.advantage)

    def primary_die(self) -> "Die":
        primary_dice = [die for die in self.dice if die.is_primary]
        if len(primary_dice) == 0:
            print(self.dice)
            raise ValueError("No primary die found in attack roll")
        if len(primary_dice) > 1:
            print(self.dice)
            raise ValueError("Multiple primary dice found in attack roll")
            
        return primary_dice[0]
    
    def last_roll_primary_die(self) -> "Die":
        primary_dice = [die for die in self.last_roll if die.is_primary]
        if len(primary_dice) == 0:
            raise ValueError("No primary die found in attack roll")
        if len(primary_dice) > 1:
            raise ValueError("Multiple primary dice found in attack roll")
        return primary_dice[0]

    def dice_to_roll(self) -> list["Die"]:
        # create a temporary list of dice to roll
        dice_to_roll = self.dice.copy()

        if self.total_advantage() == 0:
            return dice_to_roll

        # add advantage dice, as many as the absolute value of the advantage
        if self.total_advantage() > 0:
            logger.debug(f"{self.total_advantage()} advantage dice to add")
        else:
            logger.debug(f"{self.total_advantage()} disadvantage dice to add")

        # add disadvantage dice, as many as the absolute value of the advantage
        die_to_add = self.primary_die().copy()
        die_to_add.is_primary = False
        dice_to_roll.extend([die_to_add for _ in range(abs(self.total_advantage()))])

        return dice_to_roll

    def roll_with_advantage(self, advantage: int, roll: list["Die"] = []) -> list["Die"]:
        if len(roll) == 0:
            return []
        # roll the dice
        for die in roll:
            die.roll()

        # remove the n lowest dice, n being the value of the advantage. Advantage is always positive
        for _ in range(advantage):
            # remove the lowest die in dice
            min_die = min(roll, key=lambda die: die.last_roll)
            roll.remove(min_die)
            
        # check if the primary die is still in dice. If not set the first die in dice as the primary die
        if len([die for die in roll if die.is_primary]) == 0:
            roll[0].is_primary = True
            logger.debug(f"Set {roll[0]} as primary die")

        return roll
    
    def roll_with_disadvantage(self, disadvantage: int, roll: list["Die"] = []) -> list["Die"]:
        if len(roll) == 0:
            return []
        
        # roll the dice
        for die in roll:
            die.roll()
        logger.debug(f"Dice rolled:\n{'\n'.join(str(die) for die in roll)}")

        # remove the n highest dice, n being the value of the disadvantage. Disadvantage is always positive
        for _ in range(disadvantage):
            # remove the lowest die in dice
            max_die = max(roll, key=lambda die: die.last_roll)
            roll.remove(max_die)

        # check if the primary die is still in dice. If not set the first die in dice as the primary die
        if len([die for die in roll if die.is_primary]) == 0:
            roll[0].is_primary = True
            logger.debug(f"Set {roll[0]} as primary die")

        return roll

    def roll(self) -> None:
        self.last_roll = []
        dice = self.dice_to_roll()
        logger.debug(f"Dice to roll:\n{'\n'.join(str(die) for die in dice)}")

        if self.total_advantage() > 0:
            logger.debug(f"Advantage: {self.total_advantage()}")
            dice = self.roll_with_advantage(advantage=self.total_advantage(), roll=dice)

        elif self.total_advantage() < 0:
            logger.debug(f"Disadvantage: {abs(self.total_advantage())}")
            dice = self.roll_with_disadvantage(disadvantage=abs(self.total_advantage()), roll=dice)

        else:
            logger.debug("No advantage or disadvantage")
            for die in dice:
                die.roll()
            logger.debug(f"Dice rolled:\n{'\n'.join(str(die) for die in dice)}")

        logger.debug(f"Dice outcome:\n{'\n'.join(str(die) for die in dice)}")

        # the length of dice should be the same as the length of self.dice. If not raise an Error
        if len(dice) != len(self.dice):
            raise ValueError("The length of dice is not the same as the length of self.dice")
        
        self.last_roll = dice

        # check if roll failed, which is if the primary die is a 1
        if self.is_last_roll_failed():
            logger.debug("Attack roll failed!")
            return

        #check if rolll was a critical success which is if the primary die is a max roll
        if self.is_last_roll_critical():
            logger.debug("Critical success!")
            # get a copy of the primary die and make it not primary
            primary_die = self.last_roll_primary_die()
            critical_damage_die = primary_die.copy()
            critical_damage_die.is_primary = False
            critical_damage_die.roll()
            self.last_roll.append(critical_damage_die.copy())
            # while the damage rolled for the additional critical damage is max, keep rollling and adding damage
            while critical_damage_die.last_roll == critical_damage_die.sides:
                critical_damage_die.roll()
                self.last_roll.append(critical_damage_die.copy())
            return

        return

    def full_damage(self):
        if self.is_last_roll_failed():
            return 0
        return sum(die.last_roll for die in self.last_roll) + self.bonus