from dataclasses import dataclass
from .trigger import Trigger
from logging import getLogger

logger = getLogger(__name__)

@dataclass
class AttackEffect:
    name: str
    description: str
    trigger: Trigger

    def __str__(self):
        return f"{self.name}: {self.description}"
    
    def execute(self):
        pass

@dataclass
class CriticalHitCelebration(AttackEffect):
    def execute(self):
        logger.debug("Critical hit! Now that's a good hit!")