"""
Tests for combat system classes in the game.

Tests verify the behavior of BattleAction and DamageCalculator classes.
"""

import pytest
from core.entities.battler import Battler
from core.entities.character import Character
from core.entities.unit import Unit
from core.combat.battle_action import BattleAction
from core.combat.damage_calculator import DamageCalculator
from core.enums.battle_action_type import BattleActionType
from core.enums.item_type import ItemType
from core.enums.job import Job
from core.enums.unit_type import UnitType
from core.items.item import Item


class TestBattleAction:
    """Tests for BattleAction class."""

    def test_given_battle_action_when_creating_attack_action_then_has_correct_attributes(self):
        """Given BattleAction class, when creating attack action, then has correct attributes."""
        # Given
        target = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        action_type = BattleActionType.ATTACK

        # When
        action = BattleAction(action_type=action_type, target=target)

        # Then
        assert action.action_type == action_type
        assert action.target == target
        assert action.item is None

    def test_given_battle_action_when_creating_defend_action_then_has_no_target(self):
        """Given BattleAction class, when creating defend action, then has no target."""
        # Given
        action_type = BattleActionType.ATTACK  # Using ATTACK as defend placeholder

        # When
        action = BattleAction(action_type=action_type)

        # Then
        assert action.target is None
        assert action.item is None

    def test_given_battle_action_when_creating_item_action_then_has_item(self):
        """Given BattleAction class, when creating item action, then has item."""
        # Given
        target = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        item = Item(
            name="Potion",
            description="Restores HP",
            type=ItemType.SWORD,  # Using SWORD as placeholder
            stats={"hp": 50},
            job=Job.WARRIOR
        )
        action_type = BattleActionType.ITEM

        # When
        action = BattleAction(action_type=action_type, target=target, item=item)

        # Then
        assert action.action_type == action_type
        assert action.target == target
        assert action.item == item

    def test_given_battle_action_when_creating_skill_action_then_has_correct_type(self):
        """Given BattleAction class, when creating skill action, then has SKILL type."""
        # Given
        target = Unit(type=UnitType.SLIME, hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)
        expected_type = BattleActionType.SKILL

        # When
        action = BattleAction(action_type=expected_type, target=target)

        # Then
        assert action.action_type == expected_type

    def test_given_battle_action_when_creating_flee_action_then_has_correct_type(self):
        """Given BattleAction class, when creating flee action, then has FLEE type."""
        # Given
        expected_type = BattleActionType.FLEE

        # When
        action = BattleAction(action_type=expected_type)

        # Then
        assert action.action_type == expected_type
        assert action.target is None


class TestDamageCalculator:
    """Tests for DamageCalculator class."""

    def test_given_physical_attack_when_calculating_damage_then_returns_positive_value(self):
        """Given physical attack, when calculating damage, then returns positive value."""
        # Given
        attacker = Battler(hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        defender = Battler(hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)

        # When
        damage = DamageCalculator.calculate_physical_damage(attacker, defender)

        # Then
        assert damage > 0

    def test_given_physical_attack_when_attacker_has_higher_level_then_damage_increases(self):
        """Given physical attack with higher level attacker, when calculating, then damage increases."""
        # Given
        high_level_attacker = Battler(hp=100, attack=25, intelligence=15, agility=20, speed=18, level=10)
        low_level_defender = Battler(hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)
        low_level_attacker = Battler(hp=100, attack=25, intelligence=15, agility=20, speed=18, level=3)

        # When
        high_level_damage = DamageCalculator.calculate_physical_damage(high_level_attacker, low_level_defender)
        low_level_damage = DamageCalculator.calculate_physical_damage(low_level_attacker, low_level_defender)

        # Then
        assert high_level_damage > low_level_damage

    def test_given_physical_attack_when_defender_has_higher_agility_then_damage_decreases(self):
        """Given physical attack with high agility defender, when calculating, then damage decreases."""
        # Given
        attacker = Battler(hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        low_agility_defender = Battler(hp=45, attack=12, intelligence=5, agility=5, speed=10, level=3)
        high_agility_defender = Battler(hp=45, attack=12, intelligence=5, agility=30, speed=10, level=3)

        # When
        low_agi_damage = DamageCalculator.calculate_physical_damage(attacker, low_agility_defender)
        high_agi_damage = DamageCalculator.calculate_physical_damage(attacker, high_agility_defender)

        # Then
        assert low_agi_damage > high_agi_damage

    def test_given_physical_attack_when_attacker_has_higher_attack_then_damage_increases(self):
        """Given physical attack with higher attack attacker, when calculating, then damage increases."""
        # Given
        high_attack_attacker = Battler(hp=100, attack=40, intelligence=15, agility=20, speed=18, level=7)
        low_attack_attacker = Battler(hp=100, attack=10, intelligence=15, agility=20, speed=18, level=7)
        defender = Battler(hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)

        # When
        high_attack_damage = DamageCalculator.calculate_physical_damage(high_attack_attacker, defender)
        low_attack_damage = DamageCalculator.calculate_physical_damage(low_attack_attacker, defender)

        # Then
        assert high_attack_damage > low_attack_damage

    def test_given_physical_attack_when_damage_calculated_then_minimum_is_one(self):
        """Given physical attack, when damage calculated, then minimum damage is 1."""
        # Given
        weak_attacker = Battler(hp=100, attack=1, intelligence=1, agility=1, speed=1, level=1)
        high_agility_defender = Battler(hp=100, attack=1, intelligence=1, agility=100, speed=1, level=10)

        # When
        damage = DamageCalculator.calculate_physical_damage(weak_attacker, high_agility_defender)

        # Then
        assert damage >= 1

    def test_given_magic_attack_when_calculating_damage_then_returns_positive_value(self):
        """Given magic attack, when calculating damage, then returns positive value."""
        # Given
        caster = Battler(hp=60, attack=10, intelligence=30, agility=15, speed=12, level=7)
        target = Battler(hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)

        # When
        damage = DamageCalculator.calculate_magic_damage(caster, target)

        # Then
        assert damage > 0

    def test_given_magic_attack_when_caster_has_higher_intelligence_then_damage_increases(self):
        """Given magic attack with higher intelligence caster, when calculating, then damage increases."""
        # Given
        high_int_caster = Battler(hp=60, attack=10, intelligence=50, agility=15, speed=12, level=7)
        low_int_caster = Battler(hp=60, attack=10, intelligence=10, agility=15, speed=12, level=7)
        target = Battler(hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)

        # When
        high_int_damage = DamageCalculator.calculate_magic_damage(high_int_caster, target)
        low_int_damage = DamageCalculator.calculate_magic_damage(low_int_caster, target)

        # Then
        assert high_int_damage > low_int_damage

    def test_given_magic_attack_when_target_has_higher_agility_then_damage_decreases(self):
        """Given magic attack with high agility target, when calculating, then damage decreases."""
        # Given
        caster = Battler(hp=60, attack=10, intelligence=30, agility=15, speed=12, level=7)
        low_agility_target = Battler(hp=80, attack=18, intelligence=5, agility=5, speed=8, level=5)
        high_agility_target = Battler(hp=80, attack=18, intelligence=5, agility=30, speed=8, level=5)

        # When
        low_agi_damage = DamageCalculator.calculate_magic_damage(caster, low_agility_target)
        high_agi_damage = DamageCalculator.calculate_magic_damage(caster, high_agility_target)

        # Then
        assert low_agi_damage > high_agi_damage

    def test_given_magic_attack_when_caster_has_higher_level_then_damage_increases(self):
        """Given magic attack with higher level caster, when calculating, then damage increases."""
        # Given
        high_level_caster = Battler(hp=60, attack=10, intelligence=30, agility=15, speed=12, level=10)
        low_level_caster = Battler(hp=60, attack=10, intelligence=30, agility=15, speed=12, level=3)
        target = Battler(hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)

        # When
        high_level_damage = DamageCalculator.calculate_magic_damage(high_level_caster, target)
        low_level_damage = DamageCalculator.calculate_magic_damage(low_level_caster, target)

        # Then
        assert high_level_damage > low_level_damage

    def test_given_magic_attack_when_damage_calculated_then_minimum_is_one(self):
        """Given magic attack, when damage calculated, then minimum damage is 1."""
        # Given
        weak_caster = Battler(hp=60, attack=10, intelligence=1, agility=15, speed=12, level=1)
        high_agility_target = Battler(hp=80, attack=18, intelligence=5, agility=100, speed=8, level=10)

        # When
        damage = DamageCalculator.calculate_magic_damage(weak_caster, high_agility_target)

        # Then
        assert damage >= 1

    def test_given_character_and_unit_when_calculating_physical_damage_then_returns_valid_damage(self):
        """Given Character and Unit, when calculating physical damage, then returns valid damage."""
        # Given
        character = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        enemy = Unit(type=UnitType.SLIME, hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)

        # When
        damage = DamageCalculator.calculate_physical_damage(character, enemy)

        # Then
        assert damage > 0
        assert isinstance(damage, int)

    def test_given_character_and_unit_when_calculating_magic_damage_then_returns_valid_damage(self):
        """Given Character and Unit, when calculating magic damage, then returns valid damage."""
        # Given
        character = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=30, agility=20, speed=18, level=7)
        enemy = Unit(type=UnitType.SLIME, hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)

        # When
        damage = DamageCalculator.calculate_magic_damage(character, enemy)

        # Then
        assert damage > 0
        assert isinstance(damage, int)
