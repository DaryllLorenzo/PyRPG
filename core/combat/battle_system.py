from typing import List, Optional
from core.combat.battle_result import BattleResult
from core.entities.battler import Battler
from core.combat.battle_action import BattleAction
from core.combat.damage_calculator import DamageCalculator
from core.enums.battle_action_type import BattleActionType


class BattleSystem:
    """
    Main battle system managing turn-based combat.

    Handles turn order, action execution, and battle resolution.
    Supports party vs party combat with automatic turn ordering
    based on battler speed stats.

    Attributes:
        party: List of player-controlled battlers (Characters)
        enemies: List of enemy battlers (Units)
        turn_order: Ordered list of all battlers by speed
        current_turn_index: Index of the current battler's turn

    Example:
        >>> party = [cloud, tifa]  # List of Character instances
        >>> enemies = [goblin, orc]  # List of Unit instances
        >>> battle = BattleSystem(party, enemies)
        >>> result = battle.start()
        >>> if result.won:
        ...     print("Victory!")
        Victory!

    Note:
        This is a basic implementation. Advanced features like
        status effects, skills, and complex AI are pending.
    """

    def __init__(self, party: List[Battler], enemies: List[Battler]):
        """
        Initialize a new battle.

        Args:
            party: List of player-controlled battlers
            enemies: List of enemy battlers
        """
        self.party = party
        self.enemies = enemies
        self.all_battlers: List[Battler] = []
        self.turn_order: List[Battler] = []
        self.current_turn_index = 0
        self._is_running = False

    def start(self) -> BattleResult:
        """
        Start and run the battle to completion.

        Executes the main combat loop until one side is defeated
        or a party member flees successfully.

        Returns:
            BattleResult containing the outcome of the battle

        Note:
            This is a simplified implementation that automatically
            resolves combat. For manual control, use step() method.
        """
        self._initialize_battle()
        self._is_running = True

        while self._is_running:
            self.step()

        return self._get_result()

    def step(self) -> Optional[Battler]:
        """
        Execute a single turn in the battle.

        Processes the action for the current battler in turn order.
        Call this repeatedly to manually control battle flow.

        Returns:
            The battler whose turn was just processed, or None if battle ended

        Note:
            Call start() first to initialize turn order.
        """
        if not self._is_running:
            return None

        if self.current_turn_index >= len(self.turn_order):
            self._start_new_round()

        current_battler = self.turn_order[self.current_turn_index]

        if self._is_defeated(current_battler):
            self.current_turn_index += 1
            return current_battler

        action = self._determine_action(current_battler)
        self._execute_action(action, current_battler)

        if self._check_battle_end():
            self._is_running = False
            return None

        self.current_turn_index += 1
        return current_battler

    def _initialize_battle(self) -> None:
        """Set up initial turn order based on speed stats."""
        self.all_battlers = self.party + self.enemies
        self.turn_order = sorted(
            self.all_battlers,
            key=lambda b: (b.speed, b.agility),
            reverse=True
        )
        self.current_turn_index = 0

    def _start_new_round(self) -> None:
        """Reset turn order for a new round of combat."""
        self.current_turn_index = 0
        self.turn_order = sorted(
            [b for b in self.all_battlers if not self._is_defeated(b)],
            key=lambda b: (b.speed, b.agility),
            reverse=True
        )

    def _determine_action(self, battler: Battler) -> BattleAction:
        """
        Determine the action for a battler to take.

        For player party members, this would normally get input.
        For enemies, uses simple AI (attack random target).

        Args:
            battler: The battler whose turn it is

        Returns:
            BattleAction to be executed
        """
        if battler in self.party:
            return self._get_player_action(battler)
        else:
            return self._get_enemy_action(battler)

    def _get_player_action(self, battler: Battler) -> BattleAction:
        """
        Get action for a player-controlled battler.

        Currently defaults to attacking a random enemy.
        This should be replaced with actual player input.

        Args:
            battler: The player's battler

        Returns:
            BattleAction chosen by player (or default)
        """
        available_enemies = [e for e in self.enemies if not self._is_defeated(e)]
        if not available_enemies:
            return BattleAction(action_type=BattleActionType.FLEE)

        target = available_enemies[0]
        return BattleAction(action_type=BattleActionType.ATTACK, target=target)

    def _get_enemy_action(self, battler: Battler) -> BattleAction:
        """
        Get action for an enemy battler using simple AI.

        AI behavior:
        - Always attacks a random alive party member

        Args:
            battler: The enemy battler

        Returns:
            BattleAction for the enemy
        """
        available_targets = [p for p in self.party if not self._is_defeated(p)]
        if not available_targets:
            return BattleAction(action_type=BattleActionType.FLEE)

        target = available_targets[0]
        return BattleAction(action_type=BattleActionType.ATTACK, target=target)

    def _execute_action(self, action: BattleAction, attacker: Battler) -> None:
        """
        Execute a battle action.

        Handles different action types:
        - ATTACK: Deal physical damage to target
        - SKILL: Reserved for future skill system
        - ITEM: Use item (healing or buff)
        - FLEE: Attempt to escape battle

        Args:
            action: The BattleAction to execute
            attacker: The battler performing the action
        """
        if action.action_type == BattleActionType.ATTACK:
            self._execute_attack(action, attacker)
        elif action.action_type == BattleActionType.SKILL:
            pass
        elif action.action_type == BattleActionType.ITEM:
            self._execute_item_use(action, attacker)
        elif action.action_type == BattleActionType.FLEE:
            self._execute_flee(action, attacker)

    def _execute_attack(self, action: BattleAction, attacker: Battler) -> None:
        """
        Execute a physical attack action.

        Calculates damage and applies it to the target.

        Args:
            action: BattleAction with ATTACK type and valid target
            attacker: The battler performing the attack
        """
        if action.target is None or self._is_defeated(action.target):
            return

        damage = DamageCalculator.calculate_physical_damage(attacker, action.target)
        action.target.hp = max(0, action.target.hp - damage)

        self._on_damage_dealt(attacker, action.target, damage)

    def _execute_item_use(self, action: BattleAction, user: Battler) -> None:
        """
        Execute an item use action.

        Handles healing items and buffs based on item stats.

        Args:
            action: BattleAction with ITEM type and valid item
            user: The battler using the item
        """
        if action.item is None:
            return

        target = action.target if action.target else user

        if "hp" in action.item.stats:
            heal_amount = action.item.stats["hp"]
            target.hp = min(target.hp + heal_amount, target.hp + heal_amount)

    def _execute_flee(self, action: BattleAction, battler: Battler) -> None:
        """
        Execute a flee action.

        Currently always succeeds for simplicity.

        Args:
            action: BattleAction with FLEE type
            battler: The battler attempting to flee
        """
        if battler in self.party:
            self._is_running = False

    def _get_action_owner(self, action: BattleAction) -> Optional[Battler]:
        """
        Find which battler performed the action.

        Args:
            action: The action to find the owner of

        Returns:
            The battler who performed the action, or None
        """
        for battler in self.all_battlers:
            if battler in self.turn_order:
                if battler == self.turn_order[self.current_turn_index - 1]:
                    return battler
        return None

    def _is_defeated(self, battler: Battler) -> bool:
        """
        Check if a battler is defeated.

        Args:
            battler: The battler to check

        Returns:
            True if HP is 0 or below
        """
        return battler.hp <= 0

    def _check_battle_end(self) -> bool:
        """
        Check if battle end conditions are met.

        Battle ends when:
        - All enemies are defeated (player victory)
        - All party members are defeated (player loss)
        - A party member successfully flees

        Returns:
            True if battle should end
        """
        all_enemies_defeated = all(self._is_defeated(e) for e in self.enemies)
        all_party_defeated = all(self._is_defeated(p) for p in self.party)

        return all_enemies_defeated or all_party_defeated

    def _get_result(self) -> BattleResult:
        """
        Create the battle result object.

        Returns:
            BattleResult with outcome information
        """
        all_enemies_defeated = all(self._is_defeated(e) for e in self.enemies)
        survivors = [p for p in self.party if not self._is_defeated(p)]

        return BattleResult(
            won=all_enemies_defeated,
            escaped=False,
            survivors=survivors
        )

    def _on_damage_dealt(self, attacker: Battler, target: Battler, damage: int) -> None:
        """
        Callback when damage is dealt.

        Can be overridden for logging or visual effects.

        Args:
            attacker: The battler who dealt damage
            target: The battler who received damage
            damage: Amount of damage dealt
        """
        pass

    def is_running(self) -> bool:
        """
        Check if the battle is still in progress.

        Returns:
            True if battle is ongoing
        """
        return self._is_running

    def get_alive_party_members(self) -> List[Battler]:
        """
        Get list of alive party members.

        Returns:
            List of battlers from party with HP > 0
        """
        return [p for p in self.party if not self._is_defeated(p)]

    def get_alive_enemies(self) -> List[Battler]:
        """
        Get list of alive enemies.

        Returns:
            List of enemy battlers with HP > 0
        """
        return [e for e in self.enemies if not self._is_defeated(e)]
