from dataclasses import dataclass
from typing import ClassVar

from ..creature.character.berserker import Berserker
from ..creature.character.character import Character
from .trigger import Trigger

from logging import getLogger
logger = getLogger(__name__)

@dataclass
class IntensifyingFury:
    name: ClassVar[str] = "Intensifying Fury"
    description: ClassVar[str] = "If you are Raging at the beginning of your turn, roll 1 Fury Die for free."
    character: Character
    trigger: Trigger = Trigger.ON_TURN_START
    is_active: bool = False

    def __str__(self):
        return f"{self.name}: {self.description}"

    def apply(self):
        """
        Applies the Intensifying Fury feature to a character.
        If the character is raging at the beginning of their turn, this feature rolls 1 Fury Die for free.
        If all the character's Fury Dice are already at their maximum value, this feature does nothing.
        If the character's Fury Dice are not yet at their maximum value, this feature adds a new Fury Die to the character's list.
        If the character's Fury Dice are already at their maximum value and the newly rolled Fury Die is higher than the lowest value Fury Die, this feature replaces the lowest value Fury Die with the newly rolled one.
        """
        if not isinstance(self.character, Berserker):
            logger.debug("Intensifying Fury can only be applied to Berserkers")
            return
        
        if not self.character.is_raging:
            logger.debug("Intensifying Fury can only be applied to raging characters")
            return
        logger.debug("Intensifying Fury")

        if len(self.character.fury_dice) == self.character.max_fury_dice and all(die.last_roll == die.sides for die in self.character.fury_dice):
            logger.debug("character already has max fury dice")
            return
        
        fury_die = self.character.fury_die.copy()
        fury_die.roll()
        logger.debug(f"rolled a d{fury_die.sides} fury die with a result of {fury_die.last_roll}")
        
        if len(self.character.fury_dice) < max(self.character.attributes.strength.value, self.character.attributes.dexterity.value):
            self.character.fury_dice.append(fury_die)
            logger.debug("added fury die with a roll of {}".format(fury_die.last_roll))
            return
        
        min_die = min(self.character.fury_dice, key=lambda die: die.last_roll)
        if min_die.last_roll < fury_die.last_roll:
            # replace min die with fury die
            self.character.fury_dice[self.character.fury_dice.index(min_die)] = fury_die 
            logger.debug(f"replaced fury die {min_die.last_roll} with a roll of {fury_die.last_roll}")
            return
        logger.debug("did not replace fury die")
