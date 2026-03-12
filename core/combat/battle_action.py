from dataclasses import dataclass
from core.entities.battler import Battler
from core.enums.battle_action_type import BattleActionType
from core.items.item import Item

@dataclass
class BattleAction:
    """
    Represents a combat action.
    
    This dataclass encapsulates an action performed during battle, including
    the type of action, the target (if any), and any associated item.
    
    Examples:
        - BattleAction(action_type=BattleActionType.ATTACK, target=goblin)
        - BattleAction(action_type=BattleActionType.DEFEND)
        - BattleAction(action_type=BattleActionType.USE_ITEM, item=potion, target=character)
    
    Attributes:
        action_type: The type of battle action (attack, defend, use item, etc.)
        target: The target Battler affected by this action (optional, defaults to None)
        item: The Item used in this action (optional, required for USE_ITEM actions)
    
    See Also:
        - BattleActionType: Enum containing available action types
        - Battler: Base class for combat participants
        - Item: Class representing usable items in battle
    """
    action_type: BattleActionType
    target: Battler = None
    #skill
    item: Item = None