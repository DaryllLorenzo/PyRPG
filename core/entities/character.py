from dataclasses import dataclass
from core.enums.job import Job
from core.entities.battler import Battler

@dataclass
class Character(Battler):
    """
    Elaborate characters with professions and unique characteristics.

    Represents player-controlled party members, important NPCs or important enemies.
    Characters have identities (names) and defined jobs that shape their gameplay role,
    stat growth, and available abilities.

    Attributes:
        name: The character's display name (e.g., "Cloud", "Tifa", "Aerith")
        job: The Job enum defining their class (Warrior, Mage, Thief, etc.)
        
    Example:
        >>> cloud = Character(
        ...     name="Cloud",
        ...     job=Job.WARRIOR,
        ...     hp=120,
        ...     attack=25,
        ...     intelligence=15,
        ...     agility=20,
        ...     speed=18,
        ...     level=7
        ... )
        >>> print(f"{cloud.name} the {cloud.job.value} (Lv.{cloud.level})")
        Cloud the Warrior (Lv.7)

    See Also:
        - Job: Enum containing available character classes
        - Battler: Base class providing core combat stats
    """
    name: str
    job: Job