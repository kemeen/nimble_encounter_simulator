from dataclasses import dataclass, field
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player


@dataclass
class Party:
    players: list["Player"] = field(default_factory=list)

    def select_player_for_turn(self, took_turns: list["Player"]) -> "Player|None":
        available_players = [player for player in self.players if player not in took_turns and player.creature.health.is_alive]
        if len(available_players) == 0:
            return None
        return random.choice(available_players)
    
    def __str__(self) -> str:
        return ", ".join([str(player) for player in self.players])