from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from nimble_encounter_simulator.effect.trigger import Trigger

if TYPE_CHECKING:
    from ...effect.feature import Feature


@dataclass
class CharacterFeatures:
    features: list["Feature"] = field(default_factory=list)

    def features_by_trigger(self, trigger: Trigger):
        return [feature for feature in self.features if feature.trigger == trigger]
    
    def register_feature(self, feature: Feature):
        if feature in self.features:
            return
        self.features.append(feature)
