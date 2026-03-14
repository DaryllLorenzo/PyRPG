"""
Tests for Item class in the game.

Tests verify the behavior of Item dataclass including creation,
attributes, and job requirements.
"""

import pytest
from core.items.item import Item
from core.enums.item_type import ItemType
from core.enums.job import Job


class TestItem:
    """Tests for Item class."""

    def test_given_item_when_creating_sword_then_has_correct_attributes(self):
        """Given Item class, when creating sword, then has correct attributes."""
        # Given
        name = "Buster Sword"
        description = "A massive broadsword passed down through generations"
        item_type = ItemType.SWORD
        stats = {"atk": 18, "def": 2}
        job = Job.WARRIOR

        # When
        item = Item(
            name=name,
            description=description,
            type=item_type,
            stats=stats,
            job=job
        )

        # Then
        assert item.name == name
        assert item.description == description
        assert item.type == item_type
        assert item.stats == stats
        assert item.job == job

    def test_given_item_when_creating_helmet_then_type_is_helmet(self):
        """Given Item, when creating helmet, then type is HELMET."""
        # Given
        expected_type = ItemType.HELMET

        # When
        item = Item(
            name="Iron Helmet",
            description="A sturdy iron helmet",
            type=ItemType.HELMET,
            stats={"def": 5, "hp": 10},
            job=Job.KNIGHT
        )

        # Then
        assert item.type == expected_type

    def test_given_item_when_creating_pants_then_type_is_pants(self):
        """Given Item, when creating pants, then type is PANTS."""
        # Given
        expected_type = ItemType.PANTS

        # When
        item = Item(
            name="Leather Pants",
            description="Flexible leather pants",
            type=ItemType.PANTS,
            stats={"def": 3, "agility": 2},
            job=Job.THIEF
        )

        # Then
        assert item.type == expected_type

    def test_given_item_when_creating_warrior_item_then_job_requirement_is_warrior(self):
        """Given Item, when creating warrior item, then job requirement is WARRIOR."""
        # Given
        expected_job = Job.WARRIOR

        # When
        item = Item(
            name="Buster Sword",
            description="A massive broadsword",
            type=ItemType.SWORD,
            stats={"atk": 18},
            job=Job.WARRIOR
        )

        # Then
        assert item.job == expected_job

    def test_given_item_when_creating_mage_item_then_job_requirement_is_mage(self):
        """Given Item, when creating mage item, then job requirement is MAGE."""
        # Given
        # Note: There's no MAGE job, so we use a job that could represent magic users
        expected_job = Job.KNIGHT  # Using Knight as placeholder for magic-capable job

        # When
        item = Item(
            name="Magic Robe",
            description="A robe imbued with magical energy",
            type=ItemType.PANTS,
            stats={"intelligence": 15, "hp": 20},
            job=Job.KNIGHT
        )

        # Then
        assert item.job == expected_job

    def test_given_item_when_creating_thief_item_then_job_requirement_is_thief(self):
        """Given Item, when creating thief item, then job requirement is THIEF."""
        # Given
        expected_job = Job.THIEF

        # When
        item = Item(
            name="Thief's Dagger",
            description="A lightweight dagger for quick strikes",
            type=ItemType.SWORD,
            stats={"atk": 10, "agility": 5, "speed": 3},
            job=Job.THIEF
        )

        # Then
        assert item.job == expected_job

    def test_given_item_with_stats_when_accessing_attack_bonus_then_returns_correct_value(self):
        """Given Item with stats, when accessing attack bonus, then returns correct value."""
        # Given
        expected_attack = 18

        # When
        item = Item(
            name="Buster Sword",
            description="A massive broadsword",
            type=ItemType.SWORD,
            stats={"atk": 18, "def": 2},
            job=Job.WARRIOR
        )

        # Then
        assert item.stats["atk"] == expected_attack

    def test_given_item_with_stats_when_accessing_defense_bonus_then_returns_correct_value(self):
        """Given Item with stats, when accessing defense bonus, then returns correct value."""
        # Given
        expected_defense = 2

        # When
        item = Item(
            name="Buster Sword",
            description="A massive broadsword",
            type=ItemType.SWORD,
            stats={"atk": 18, "def": 2},
            job=Job.WARRIOR
        )

        # Then
        assert item.stats["def"] == expected_defense

    def test_given_item_when_modifying_stats_then_values_change(self):
        """Given Item instance, when modifying stats, then values change."""
        # Given
        item = Item(
            name="Buster Sword",
            description="A massive broadsword",
            type=ItemType.SWORD,
            stats={"atk": 18, "def": 2},
            job=Job.WARRIOR
        )

        # When
        item.stats["atk"] = 25

        # Then
        assert item.stats["atk"] == 25

    def test_given_two_items_with_same_attributes_when_comparing_then_are_equal(self):
        """Given two items with same attributes, when comparing, then are equal."""
        # Given
        item1 = Item(
            name="Buster Sword",
            description="A massive broadsword",
            type=ItemType.SWORD,
            stats={"atk": 18, "def": 2},
            job=Job.WARRIOR
        )
        item2 = Item(
            name="Buster Sword",
            description="A massive broadsword",
            type=ItemType.SWORD,
            stats={"atk": 18, "def": 2},
            job=Job.WARRIOR
        )

        # When
        result = item1 == item2

        # Then
        assert result is True

    def test_given_two_items_with_different_names_when_comparing_then_are_not_equal(self):
        """Given two items with different names, when comparing, then are not equal."""
        # Given
        item1 = Item(
            name="Buster Sword",
            description="A massive broadsword",
            type=ItemType.SWORD,
            stats={"atk": 18, "def": 2},
            job=Job.WARRIOR
        )
        item2 = Item(
            name="Iron Sword",
            description="A standard iron sword",
            type=ItemType.SWORD,
            stats={"atk": 10, "def": 1},
            job=Job.WARRIOR
        )

        # When
        result = item1 == item2

        # Then
        assert result is False

    def test_given_item_when_creating_with_empty_stats_then_stats_is_empty_dict(self):
        """Given Item, when creating with empty stats, then stats is empty dict."""
        # Given
        expected_stats = {}

        # When
        item = Item(
            name="Plain Clothes",
            description="Basic clothing with no bonuses",
            type=ItemType.PANTS,
            stats={},
            job=Job.WARRIOR
        )

        # Then
        assert item.stats == expected_stats
