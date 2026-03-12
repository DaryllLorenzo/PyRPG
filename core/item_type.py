from enum import Enum

class ItemType(Enum):
    """
    Type of items available

    Example:
        >>> item_type = ItemType.SWORD
        >>> print(f"{item_type.value}")
        Sword
    """
    SWORD = "Sword"
    PANTS = "Pants"
    HELMET = "Helmet"