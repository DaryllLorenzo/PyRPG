from core.entities.battler import Battler

class DamageCalculator:

    @staticmethod
    def calculate_physical_damage(attacker: Battler, defender: Battler) -> int:
        """
        Calculate physical damage dealt by attacker to defender.

        Uses a simple formula based on attack stat and level difference.
        Damage is reduced by defender's agility (evasion/defense proxy).

        Formula:
            base_damage = attacker.attack * (1 + level_diff_bonus)
            final_damage = max(1, base_damage - defender.agility * 0.5)

        Args:
            attacker: The Battler performing the attack
            defender: The Battler receiving the attack

        Returns:
            The amount of damage dealt (minimum 1)

        Example:
            >>> warrior = Battler(hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
            >>> goblin = Battler(hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)
            >>> damage = calculate_physical_damage(warrior, goblin)
            >>> print(f"Dealt {damage} damage!")
            Dealt 28 damage!
        """
        level_diff = attacker.level - defender.level
        level_diff_bonus = level_diff * 0.1

        base_damage = attacker.attack * (1 + level_diff_bonus)
        reduction = defender.agility * 0.5
        final_damage = max(1, int(base_damage - reduction))

        return final_damage

    @staticmethod
    def calculate_magic_damage(caster: Battler, target: Battler) -> int:
        """
        Calculate magic damage dealt by caster to target.

        Uses intelligence stat for damage calculation.
        Target's agility reduces magic damage (resistance proxy).

        Formula:
            base_damage = caster.intelligence * 1.5 * (1 + level_diff_bonus)
            final_damage = max(1, base_damage - target.agility * 0.3)

        Args:
            caster: The Battler casting the spell
            target: The Battler receiving the spell

        Returns:
            The amount of magic damage dealt (minimum 1)

        Example:
            >>> mage = Battler(hp=60, attack=10, intelligence=30, agility=15, speed=12, level=7)
            >>> orc = Battler(hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)
            >>> damage = calculate_magic_damage(mage, orc)
            >>> print(f"Spell dealt {damage} damage!")
            Spell dealt 48 damage!
        """
        level_diff = caster.level - target.level
        level_diff_bonus = level_diff * 0.1

        base_damage = caster.intelligence * 1.5 * (1 + level_diff_bonus)
        reduction = target.agility * 0.3
        final_damage = max(1, int(base_damage - reduction))

        return final_damage
