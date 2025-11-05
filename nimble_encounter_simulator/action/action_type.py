from enum import StrEnum


class ActionType(StrEnum):
    ATTACK = "Attack"
    ASSESS = "Assess"
    MOVE = "Move"
    CAST_SPELL = "Cast Spell"