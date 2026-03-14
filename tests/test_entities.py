"""
Tests for entity classes in the game.

Tests verify the behavior of Battler, Character, and Unit classes.
"""

import pytest
from dataclasses import dataclass
from core.entities.battler import Battler
from core.entities.character import Character
from core.entities.unit import Unit
from core.enums.job import Job
from core.enums.unit_type import UnitType


class TestBattler:
    """Tests for Battler base class."""

    def test_given_battler_when_creating_instance_then_has_all_required_attributes(self):
        """Given Battler class, when creating instance, then has all required attributes."""
        # Given
        hp = 100
        attack = 25
        intelligence = 15
        agility = 20
        speed = 18
        level = 7

        # When
        battler = Battler(
            hp=hp,
            attack=attack,
            intelligence=intelligence,
            agility=agility,
            speed=speed,
            level=level
        )

        # Then
        assert battler.hp == hp
        assert battler.attack == attack
        assert battler.intelligence == intelligence
        assert battler.agility == agility
        assert battler.speed == speed
        assert battler.level == level

    def test_given_battler_when_modifying_hp_then_value_changes(self):
        """Given Battler instance, when modifying hp, then value changes accordingly."""
        # Given
        battler = Battler(hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        new_hp = 50

        # When
        battler.hp = new_hp

        # Then
        assert battler.hp == new_hp

    def test_given_battler_when_taking_damage_then_hp_decreases(self):
        """Given Battler instance, when taking damage, then hp decreases."""
        # Given
        battler = Battler(hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        damage = 30

        # When
        battler.hp -= damage

        # Then
        assert battler.hp == 70

    def test_given_battler_when_receiving_healing_then_hp_increases(self):
        """Given Battler instance, when receiving healing, then hp increases."""
        # Given
        battler = Battler(hp=50, attack=25, intelligence=15, agility=20, speed=18, level=7)
        healing = 30

        # When
        battler.hp += healing

        # Then
        assert battler.hp == 80


class TestCharacter:
    """Tests for Character class."""

    def test_given_character_when_creating_with_job_then_has_correct_attributes(self):
        """Given Character class, when creating with job, then has correct attributes."""
        # Given
        name = "Cloud"
        job = Job.WARRIOR
        hp = 120
        attack = 25
        intelligence = 15
        agility = 20
        speed = 18
        level = 7

        # When
        character = Character(
            name=name,
            job=job,
            hp=hp,
            attack=attack,
            intelligence=intelligence,
            agility=agility,
            speed=speed,
            level=level
        )

        # Then
        assert character.name == name
        assert character.job == job
        assert character.hp == hp
        assert character.attack == attack
        assert character.intelligence == intelligence
        assert character.agility == agility
        assert character.speed == speed
        assert character.level == level

    def test_given_character_when_creating_warrior_then_job_is_warrior(self):
        """Given Character, when creating warrior, then job is WARRIOR."""
        # Given
        expected_job = Job.WARRIOR

        # When
        character = Character(name="Warrior", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=1)

        # Then
        assert character.job == expected_job

    def test_given_character_when_creating_knight_then_job_is_knight(self):
        """Given Character, when creating knight, then job is KNIGHT."""
        # Given
        expected_job = Job.KNIGHT

        # When
        character = Character(name="Knight", job=Job.KNIGHT, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=1)

        # Then
        assert character.job == expected_job

    def test_given_character_when_creating_monk_then_job_is_monk(self):
        """Given Character, when creating monk, then job is MONK."""
        # Given
        expected_job = Job.MONK

        # When
        character = Character(name="Monk", job=Job.MONK, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=1)

        # Then
        assert character.job == expected_job

    def test_given_character_when_creating_thief_then_job_is_thief(self):
        """Given Character, when creating thief, then job is THIEF."""
        # Given
        expected_job = Job.THIEF

        # When
        character = Character(name="Thief", job=Job.THIEF, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=1)

        # Then
        assert character.job == expected_job

    def test_given_character_when_leveling_up_then_level_increases(self):
        """Given Character instance, when leveling up, then level increases."""
        # Given
        character = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        new_level = 8

        # When
        character.level = new_level

        # Then
        assert character.level == new_level

    def test_given_two_characters_with_same_attributes_when_comparing_then_are_equal(self):
        """Given two characters with same attributes, when comparing, then are equal."""
        # Given
        character1 = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        character2 = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)

        # When
        result = character1 == character2

        # Then
        assert result is True

    def test_given_two_characters_with_different_names_when_comparing_then_are_not_equal(self):
        """Given two characters with different names, when comparing, then are not equal."""
        # Given
        character1 = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        character2 = Character(name="Sephiroth", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)

        # When
        result = character1 == character2

        # Then
        assert result is False


class TestUnit:
    """Tests for Unit class."""

    def test_given_unit_when_creating_with_type_then_has_correct_attributes(self):
        """Given Unit class, when creating with type, then has correct attributes."""
        # Given
        unit_type = UnitType.SLIME
        hp = 45
        attack = 12
        intelligence = 5
        agility = 15
        speed = 10
        level = 3

        # When
        unit = Unit(
            type=unit_type,
            hp=hp,
            attack=attack,
            intelligence=intelligence,
            agility=agility,
            speed=speed,
            level=level
        )

        # Then
        assert unit.type == unit_type
        assert unit.hp == hp
        assert unit.attack == attack
        assert unit.intelligence == intelligence
        assert unit.agility == agility
        assert unit.speed == speed
        assert unit.level == level

    def test_given_unit_when_creating_slime_then_type_is_slime(self):
        """Given Unit, when creating slime, then type is SLIME."""
        # Given
        expected_type = UnitType.SLIME

        # When
        unit = Unit(type=UnitType.SLIME, hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)

        # Then
        assert unit.type == expected_type

    def test_given_unit_when_creating_orc_then_type_is_orc(self):
        """Given Unit, when creating orc, then type is ORC."""
        # Given
        expected_type = UnitType.ORC

        # When
        unit = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)

        # Then
        assert unit.type == expected_type

    def test_given_unit_when_creating_goblin_then_type_is_goblin(self):
        """Given Unit, when creating goblin, then type is GOBLIN."""
        # Given
        expected_type = UnitType.GOBLIN

        # When
        unit = Unit(type=UnitType.GOBLIN, hp=40, attack=15, intelligence=8, agility=20, speed=15, level=4)

        # Then
        assert unit.type == expected_type

    def test_given_unit_when_taking_damage_then_hp_decreases(self):
        """Given Unit instance, when taking damage, then hp decreases."""
        # Given
        unit = Unit(type=UnitType.SLIME, hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)
        damage = 20

        # When
        unit.hp -= damage

        # Then
        assert unit.hp == 25

    def test_given_unit_when_defeated_then_hp_is_zero_or_below(self):
        """Given Unit instance, when defeated, then hp is zero or below."""
        # Given
        unit = Unit(type=UnitType.SLIME, hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)
        damage = 50

        # When
        unit.hp -= damage

        # Then
        assert unit.hp <= 0
