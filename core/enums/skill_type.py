from enum import Enum


class SkillType(Enum):
    """
    Type of skills available in the game

    Example:
        >>> skill_type = SkillType.PHYSICAL
        >>> print(f"{skill_type.value}")
        Physical
    """

    PHYSICAL = "Physical"
    MAGIC = "Magic"
    SUPPORT = "Support"
    HEALING = "Healing"
