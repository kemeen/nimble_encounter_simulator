from enum import StrEnum

class Trigger(StrEnum):
    AUTOMATIC = "automatic"
    ON_HIT = "on_hit"
    ON_DAMAGE = "on_damage"
    ON_CRIT = "on_crit"
    ON_MISS = "on_miss"
    ON_DEATH = "on_death"
    ON_EQUIP = "on_equip"
    ON_UNEQUIP = "on_unequip"
    ON_USE = "on_use"
    ON_HEAL = "on_heal"
    ON_TURN_START = "on_turn_start"
    ON_TURN_END = "on_turn_end"
    ON_ROUND_START = "on_round_start"
    ON_ROUND_END = "on_round_end"