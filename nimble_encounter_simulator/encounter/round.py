from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .monster_handler import MonsterHandler
from ..creature.monster import Monster, MonsterRole
from .turn import Actor, Turn
from ..logging_setup import get_named_console_logger

logger = get_named_console_logger(__name__)

if TYPE_CHECKING:
    from .party import Party
    from .player import Player
    

@dataclass
class Round:
    number: int
    party: "Party"
    enemies: list["MonsterHandler"] = field(default_factory=list)
    finished_turns: list["Turn"] = field(default_factory=list)
    available_turns: list["Turn"] = field(default_factory=list)
 

    def initialize_turns(self):
        # initialize the available turns, order is not important. 
        logger.debug(f"Initializing turns for round {self.number}")
        # Each player in the party gets a turn
        self.available_turns = [Turn(actor=player, party=self.party, enemies=self.enemies) for player in self.party.players if player.creature.health.is_alive]
        # each normal monster gets a turn 
        self.available_turns += [Turn(actor=handler, party=self.party, enemies=self.enemies) for handler in self.enemies if handler.monster.role is not MonsterRole.LEGENDARY]
        if self.legendary_monster_present():
            # legendary monsters get one turn per player in the party.
            self.available_turns += [Turn(actor=handler, party=self.party, enemies=self.enemies) for handler in self.enemies if handler.monster.role is MonsterRole.LEGENDARY for _ in range(len(self.party.players))]


    def run(self):
        logger.debug(f"{'='*20} Running round {self.number} {'='*20}")
        self.initialize_turns()
        while len(self.available_turns) > 0:
            turn = self.next_turn()
            if turn is None:
                return
            logger.debug(f"{'-'*10} Turn for {turn.actor} {'-'*10}")
            turn = turn.take_turn()
            self.finished_turns.append(turn)

    def get_available_turn_by_actor(self, actor: "Actor") -> Turn:
        for turn in self.available_turns:
            if turn.actor == actor:
                return turn

        raise ValueError(f"No available turn for actor {actor}")

    def next_turn(self) -> "Turn|None":
        from .player import Player
        
        if len(self.available_turns) == 0:
            return
        
        if not self.legendary_monster_present():
            # let the party take turns until all have taken turns, after that let the monsters take their turns
            players_that_took_turns = [turn.actor for turn in self.finished_turns if isinstance(turn.actor, Player)]
            actor = self.party.select_player_for_turn(took_turns=players_that_took_turns)
            if actor is None:
                return self.available_turns.pop(0)
            turn = self.get_available_turn_by_actor(actor=actor)
            self.available_turns.remove(turn)
            return turn
        
        # legendary monsters get one turn per player in the party.
        if isinstance(self.finished_turns[-1].actor, Player):
            # get turn for a legendary monster

            turn = self.get_available_turn_by_actor(actor=actor)
            self.available_turns.remove(turn)
            return turn

        return self.available_turns.pop(0)
        
    def get_turn_for_legendary_monster(self) -> "Turn":
        if not self.legendary_monster_present():
            raise ValueError("No legendary monster present")
        for turn in self.available_turns:
            if isinstance(turn.actor.creature, Monster) and turn.actor.creature.role is MonsterRole.LEGENDARY:
                return turn

        raise ValueError("No legendary monster present")

    def players_that_took_turns(self) -> list["Player"]:
        return [turn.actor for turn in self.finished_turns if isinstance(turn.actor, Player)]
        
    def legendary_monster_present(self) -> bool:
        return any(handler.monster.role == MonsterRole.LEGENDARY for handler in self.enemies if handler.monster.is_alive)