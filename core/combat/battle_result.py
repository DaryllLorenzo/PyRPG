from dataclasses import dataclass, field
from core.entities.battler import Battler
from typing import List

@dataclass
class BattleResult:
    """
    Result of a completed battle.

    Attributes:
        won: Whether the player's party won the battle
        escaped: Whether the battle ended by fleeing
        survivors: List of surviving battlers from the player's party
    """
    won: bool
    escaped: bool = False
    survivors: List[Battler] = field(default_factory=list)