from dataclasses import dataclass

from core.enums.skill_type import SkillType


@dataclass
class Skill:
    """
    Represents a skill or ability that can be used in combat.

    Skills are special abilities that characters can use during battle.
    Each skill has a name, description, type, MP cost, power, and optional
    status effects. Skills can be physical attacks, magic spells, healing
    abilities, or support buffs.

    Attributes:
        name: The skill's display name (e.g., "Brave Slash", "Cure", "Fire")
        description: A brief description of what the skill does
        type: The SkillType enum defining its category (Physical, Magic, etc.)
        mp_cost: The MP cost to use this skill (0 for physical skills)
        power: The base power of the skill (multiplier for damage/healing)
        status_effect: Optional status effect name to apply (e.g., "Poison", "Sleep")
        status_chance: Chance to apply status effect (0.0 to 1.0)

    Example:
        >>> brave_slash = Skill(
        ...     name="Brave Slash",
        ...     description="A powerful slash that may inflict poison",
        ...     type=SkillType.PHYSICAL,
        ...     mp_cost=5,
        ...     power=1.5,
        ...     status_effect="Poison",
        ...     status_chance=0.3
        ... )
        >>> print(f"{brave_slash.name} ({brave_slash.type.value})")
        Brave Slash (Physical)
        >>> print(f"MP Cost: {brave_slash.mp_cost}")
        MP Cost: 5
        >>> print(f"Power: {brave_slash.power}x")
        Power: 1.5x

    See Also:
        - SkillType: Enum containing available skill categories
        - Character: Class that can learn and use skills
    """

    name: str
    description: str
    type: SkillType
    mp_cost: int
    power: float
    status_effect: str = None
    status_chance: float = 0.0
