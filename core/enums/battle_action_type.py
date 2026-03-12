from enum import Enum

class BattleActionType(Enum):
    """
    Type of battle actions

    Example:
        >>> battle_action_type = BattleActionType.ATTACK
        >>> print(f"{battle_action_type.value}")
        Attack
    """
    ATTACK = "Attack"
    SKILL = "Skill"
    ITEM = "Item"
    FLEE = "Flee"