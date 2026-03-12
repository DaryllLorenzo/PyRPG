from dataclasses import dataclass

from core.entities.battler import Battler
from core.enums.unit_type import UnitType

@dataclass
class Unit(Battler):
    """
    Basic combat unit, designed for mobs and generic enemies.

    Represents standard enemy encounters in the game world. Units are simpler
    than characters, typically controlled by AI and used for random encounters
    or field mobs.

    Attributes:
        type: The UnitType enum defining this unit's category (beast, undead, etc.)
        
    Example:
        >>> goblin = Unit(
        ...     type=UnitType.BEAST,
        ...     hp=45,
        ...     attack=12,
        ...     intelligence=5,
        ...     agility=15,
        ...     speed=10,
        ...     level=3
        ... )
        >>> print(f"A level {goblin.level} {goblin.type.value} appears!")
        A level 3 Beast appears!

    Note:
        Units typically don't have names or jobs - they are defined by their
        type and stats. For named bosses or important NPCs, consider using
        Character class instead.
    """
    
    type: UnitType