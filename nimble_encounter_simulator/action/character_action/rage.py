from dataclasses import dataclass, field
from typing import ClassVar
from logging import getLogger

from ..action_cost import ActionCost
from ..action_ressource import ActionRessource
from .character_action import ActionType
from ...creature.character.berserker import Berserker
from ...creature.character.character import Character
from ...creature.monster.monster import Monster
from ...encounter.turn import Turn
from ...roll.advantage import Advantage
logger = getLogger(__name__)

@dataclass
class Rage:
    character: "Character"
    name: ClassVar[str] = "Rage"
    description: ClassVar[str] = "Break out into a furious rage!"
    cost: ClassVar[list[ActionCost]] = [ActionCost(amount=1, ressource=ActionRessource.ACTION_POINT)]
    action_type: ClassVar[ActionType] = ActionType.CAST_SPELL
    advantage: list["Advantage"] = field(default_factory=list)
    targets: list["Character|Monster"] = field(default_factory=list)

    def __str__(self):
        return f"{self.name}: {self.description}"
    
    def execute(self, turn: "Turn"):
        # if the creature is not a berserker do nothing
        creature = turn.actor.creature
        if not isinstance(creature, Berserker):
            return
        
        # set the berserkers is_raging attribute to True
        creature.is_raging = True
        
        # if all fury dice are maxed out do not do anything
        if len(creature.fury_dice) == creature.max_fury_dice and all(die.last_roll == die.sides for die in creature.fury_dice):
            return
        
        # get a copy of the berserkers fury die
        fury_die = creature.fury_die.copy()

        # roll the fury die
        fury_die.roll()
        logger.debug(f"{creature.name} rolled a d{fury_die.sides} fury die with a result of {fury_die.last_roll}!")

        # add the fury die to the berserkers fury dice if there less than the max number of fury dice
        if len(creature.fury_dice) < creature.max_fury_dice:
            creature.fury_dice.append(fury_die)
            logger.debug(f"{creature.name} added a fury die with a result of {fury_die.last_roll}!")
            return

        # replace the lowest fury die with the rolled fury die if it is higher
        min_die = min(creature.fury_dice, key=lambda die: die.last_roll)
        if min_die.last_roll < fury_die.last_roll:
            logger.debug(f"{creature.name} replaced a fury die with a value of {min_die.last_roll} with a fury die with a value of {fury_die.last_roll}!")
            min_die.last_roll = fury_die.last_roll
            return

        logger.debug(f"{creature.name} did not add or replace a fury die!")

