from dataclasses import dataclass

from core.item_type import ItemType
from core.job import Job

@dataclass
class Item:
    """
    Represents an equippable item for characters in the game.

    Items provide stat bonuses and can only be equipped by characters of specific jobs.
    Each item has a name, description, type, job requirement, and a dictionary of stats it grants.

    Attributes:
        name: The item's display name (e.g., "Buster Sword", "Mythril Armor")
        description: A brief description of the item's appearance or lore
        type: The ItemType enum defining its category (Sword, Helmet, Robe, etc.)
        stats: Dictionary of stat bonuses the item provides
               (e.g., {"hp": 15, "atk": 5, "def": 3})
        job: The Job enum required to equip this item (Warrior, Mage, Thief, etc.)

    Example:
        >>> buster_sword = Item(
        ...     name="Buster Sword",
        ...     description="A massive broadsword passed down through generations",
        ...     type=ItemType.SWORD,
        ...     stats={"atk": 18, "def": 2},
        ...     job=Job.WARRIOR
        ... )
        >>> print(f"{buster_sword.name} ({buster_sword.type.value})")
        Buster Sword (Sword)
        >>> print(f"Required job: {buster_sword.job.value}")
        Required job: Warrior
        >>> print(f"Attack bonus: +{buster_sword.stats['atk']}")
        Attack bonus: +18

    See Also:
        - ItemType: Enum containing available item categories
        - Job: Enum containing character classes that can equip items
        - Character: Class that can equip items based on their job
    """
    name: str
    description: str
    type: ItemType
    stats: dict
    job: Job