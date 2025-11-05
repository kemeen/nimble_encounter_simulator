from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from logging import getLogger
logger = getLogger(__name__)

if TYPE_CHECKING:
    from ..creature.character.character import Character
    from ..action.character_action.character_action import CharacterAction
    from .turn import Turn
    from ..strategy.strategy import Strategy


@dataclass
class Player:
    creature: "Character"
    strategy: "Strategy"
    actions: list["CharacterAction"] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.creature.name} ({self.strategy})"
    
    def register_action(self, action: "CharacterAction"):
        self.actions.append(action)
    
    def process_turn(self, turn: "Turn") -> "Turn":
        while not turn.is_finished:
            # use strategy to pick actions
            # execute actions
            self.strategy.available_actions = self.actions
            action = self.strategy.choose_action()
            logger.debug(f"{self.creature.name} chooses the {action.name} action")
            action.execute()
            self.strategy.actions_taken.append(action)
            turn.actions_taken.append(action)
            # sleep(.2)
        
        return turn

    def take_turn(self, turn: "Turn") -> "Turn":
        logger.debug(f"{self}'s turn")
        self.on_turn_start()
        turn = self.process_turn(turn)
        self.on_turn_end()
        return turn
    
    def on_turn_start(self):
        self.creature.on_turn_start()

    def on_turn_end(self):
        self.creature.on_turn_end()
        self.strategy.reset()