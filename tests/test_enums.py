"""
Tests for enumeration types in the game.

Tests verify that all enum values are correctly defined and accessible.
"""

import pytest
from core.enums.job import Job
from core.enums.item_type import ItemType
from core.enums.unit_type import UnitType
from core.enums.battle_action_type import BattleActionType
from core.enums.skill_type import SkillType


class TestJob:
    """Tests for Job enumeration."""

    def test_given_job_enum_when_accessing_warrior_then_returns_correct_value(self):
        """Given Job enum, when accessing WARRIOR, then returns correct value."""
        # Given
        expected_value = "Warrior"

        # When
        result = Job.WARRIOR.value

        # Then
        assert result == expected_value

    def test_given_job_enum_when_accessing_knight_then_returns_correct_value(self):
        """Given Job enum, when accessing KNIGHT, then returns correct value."""
        # Given
        expected_value = "Knight"

        # When
        result = Job.KNIGHT.value

        # Then
        assert result == expected_value

    def test_given_job_enum_when_accessing_monk_then_returns_correct_value(self):
        """Given Job enum, when accessing MONK, then returns correct value."""
        # Given
        expected_value = "Monk"

        # When
        result = Job.MONK.value

        # Then
        assert result == expected_value

    def test_given_job_enum_when_accessing_thief_then_returns_correct_value(self):
        """Given Job enum, when accessing THIEF, then returns correct value."""
        # Given
        expected_value = "Thief"

        # When
        result = Job.THIEF.value

        # Then
        assert result == expected_value

    def test_given_job_enum_when_listing_all_jobs_then_returns_four_jobs(self):
        """Given Job enum, when listing all jobs, then returns four job types."""
        # Given
        expected_count = 4

        # When
        result = list(Job)

        # Then
        assert len(result) == expected_count


class TestItemType:
    """Tests for ItemType enumeration."""

    def test_given_item_type_enum_when_accessing_sword_then_returns_correct_value(self):
        """Given ItemType enum, when accessing SWORD, then returns correct value."""
        # Given
        expected_value = "Sword"

        # When
        result = ItemType.SWORD.value

        # Then
        assert result == expected_value

    def test_given_item_type_enum_when_accessing_pants_then_returns_correct_value(self):
        """Given ItemType enum, when accessing PANTS, then returns correct value."""
        # Given
        expected_value = "Pants"

        # When
        result = ItemType.PANTS.value

        # Then
        assert result == expected_value

    def test_given_item_type_enum_when_accessing_helmet_then_returns_correct_value(self):
        """Given ItemType enum, when accessing HELMET, then returns correct value."""
        # Given
        expected_value = "Helmet"

        # When
        result = ItemType.HELMET.value

        # Then
        assert result == expected_value


class TestUnitType:
    """Tests for UnitType enumeration."""

    def test_given_unit_type_enum_when_accessing_slime_then_returns_correct_value(self):
        """Given UnitType enum, when accessing SLIME, then returns correct value."""
        # Given
        expected_value = "Slime"

        # When
        result = UnitType.SLIME.value

        # Then
        assert result == expected_value

    def test_given_unit_type_enum_when_accessing_orc_then_returns_correct_value(self):
        """Given UnitType enum, when accessing ORC, then returns correct value."""
        # Given
        expected_value = "Orc"

        # When
        result = UnitType.ORC.value

        # Then
        assert result == expected_value

    def test_given_unit_type_enum_when_accessing_goblin_then_returns_correct_value(self):
        """Given UnitType enum, when accessing GOBLIN, then returns correct value."""
        # Given
        expected_value = "Goblin"

        # When
        result = UnitType.GOBLIN.value

        # Then
        assert result == expected_value


class TestBattleActionType:
    """Tests for BattleActionType enumeration."""

    def test_given_battle_action_type_enum_when_accessing_attack_then_returns_correct_value(self):
        """Given BattleActionType enum, when accessing ATTACK, then returns correct value."""
        # Given
        expected_value = "Attack"

        # When
        result = BattleActionType.ATTACK.value

        # Then
        assert result == expected_value

    def test_given_battle_action_type_enum_when_accessing_skill_then_returns_correct_value(self):
        """Given BattleActionType enum, when accessing SKILL, then returns correct value."""
        # Given
        expected_value = "Skill"

        # When
        result = BattleActionType.SKILL.value

        # Then
        assert result == expected_value

    def test_given_battle_action_type_enum_when_accessing_item_then_returns_correct_value(self):
        """Given BattleActionType enum, when accessing ITEM, then returns correct value."""
        # Given
        expected_value = "Item"

        # When
        result = BattleActionType.ITEM.value

        # Then
        assert result == expected_value

    def test_given_battle_action_type_enum_when_accessing_flee_then_returns_correct_value(self):
        """Given BattleActionType enum, when accessing FLEE, then returns correct value."""
        # Given
        expected_value = "Flee"

        # When
        result = BattleActionType.FLEE.value

        # Then
        assert result == expected_value


class TestSkillType:
    """Tests for SkillType enumeration."""

    def test_given_skill_type_enum_when_accessing_physical_then_returns_correct_value(self):
        """Given SkillType enum, when accessing PHYSICAL, then returns correct value."""
        # Given
        expected_value = "Physical"

        # When
        result = SkillType.PHYSICAL.value

        # Then
        assert result == expected_value

    def test_given_skill_type_enum_when_accessing_magic_then_returns_correct_value(self):
        """Given SkillType enum, when accessing MAGIC, then returns correct value."""
        # Given
        expected_value = "Magic"

        # When
        result = SkillType.MAGIC.value

        # Then
        assert result == expected_value

    def test_given_skill_type_enum_when_accessing_support_then_returns_correct_value(self):
        """Given SkillType enum, when accessing SUPPORT, then returns correct value."""
        # Given
        expected_value = "Support"

        # When
        result = SkillType.SUPPORT.value

        # Then
        assert result == expected_value

    def test_given_skill_type_enum_when_accessing_healing_then_returns_correct_value(self):
        """Given SkillType enum, when accessing HEALING, then returns correct value."""
        # Given
        expected_value = "Healing"

        # When
        result = SkillType.HEALING.value

        # Then
        assert result == expected_value
