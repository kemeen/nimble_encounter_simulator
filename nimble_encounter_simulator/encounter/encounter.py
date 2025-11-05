from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .monster_handler import MonsterHandler
    from .round import Party
    from .round import Round

from ..logging_setup import get_named_console_logger

logger = get_named_console_logger(__name__)

@dataclass
class Encounter:
    party: "Party"
    enemies: list["MonsterHandler"] = field(default_factory=list)
    rounds: list["Round"] = field(default_factory=list)

    def run(self, rounds=5):
        from .round import Round
        while not self.is_finished():
            # initialize a new round
            round_number = len(self.rounds) + 1
            current_round = Round(number=round_number, party=self.party, enemies=self.enemies)
            current_round.run()
            self.rounds.append(current_round)
            if round_number == rounds:
                return

    def is_finished(self) -> bool:
        # the encounter is finished if either all enemies are dead or all characters in the party are dead
        if all(not handler.monster.is_alive for handler in self.enemies):
            logger.debug("All enemies dead!")
            return True
        if all(not player.creature.health.is_alive for player in self.party.players):
            logger.debug("All characters dead!")
            return True
        return False



