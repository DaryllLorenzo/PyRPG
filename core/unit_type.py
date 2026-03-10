from enum import Enum

class UnitType(Enum):
    """
    Type of units available

    Example:
        >>> unit_type = UnitType.SLIME
        >>> print(f"{unit_type.value}")
        Slime
    """

    SLIME = "Slime"
    ORC = "Orc"
    GOBLIN = "Goblin"