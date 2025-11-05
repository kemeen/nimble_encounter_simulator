from dataclasses import dataclass

from .action_ressource import ActionRessource


@dataclass
class ActionCost:
    amount: int
    ressource: ActionRessource