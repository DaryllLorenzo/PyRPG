"""
Tests for Party class in the game.

Tests verify the behavior of the Party class for managing groups of battlers.
"""

import pytest
from core.entities.battler import Battler
from core.entities.character import Character
from core.entities.unit import Unit
from core.entities.party import Party
from core.enums.job import Job
from core.enums.unit_type import UnitType


class TestParty:
    """Tests for Party class."""

    def test_given_party_when_creating_empty_then_has_no_members(self):
        """Given Party class, when creating empty, then has no members."""
        # Given / When
        party = Party()

        # Then
        assert len(party.members) == 0
        assert party.is_alive() is False
        assert party.is_defeated() is True

    def test_given_party_when_creating_with_members_then_has_correct_count(self):
        """Given Party class, when creating with members, then has correct count."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)
        aerith = Character(name="Aerith", job=Job.KNIGHT, hp=80, attack=18, intelligence=28, agility=18, speed=16, level=7)

        # When
        party = Party([cloud, tifa, aerith])

        # Then
        assert len(party.members) == 3
        assert party.is_alive() is True
        assert party.is_defeated() is False

    def test_given_party_when_adding_member_then_count_increases(self):
        """Given Party instance, when adding member, then count increases."""
        # Given
        party = Party()
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)

        # When
        party.add_member(cloud)

        # Then
        assert len(party.members) == 1
        assert cloud in party

    def test_given_party_when_removing_member_then_count_decreases(self):
        """Given Party instance, when removing member, then count decreases."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)
        party = Party([cloud, tifa])

        # When
        result = party.remove_member(cloud)

        # Then
        assert result is True
        assert len(party.members) == 1
        assert cloud not in party

    def test_given_party_when_removing_nonexistent_member_then_returns_false(self):
        """Given Party instance, when removing nonexistent member, then returns False."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        party = Party([cloud])
        sep = Character(name="Sephiroth", job=Job.WARRIOR, hp=150, attack=35, intelligence=25, agility=25, speed=23, level=10)

        # When
        result = party.remove_member(sep)

        # Then
        assert result is False
        assert len(party.members) == 1

    def test_given_party_when_members_take_damage_then_get_alive_returns_correct(self):
        """Given Party instance, when members take damage, then get_alive returns correct."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)
        aerith = Character(name="Aerith", job=Job.KNIGHT, hp=80, attack=18, intelligence=28, agility=18, speed=16, level=7)
        party = Party([cloud, tifa, aerith])

        # When
        tifa.hp = 0  # Tifa defeated
        aerith.hp = 30  # Aerith injured but alive

        # Then
        alive = party.get_alive_members()
        assert len(alive) == 2
        assert cloud in alive
        assert aerith in alive
        assert tifa not in alive

    def test_given_party_when_all_defeated_then_is_defeated_returns_true(self):
        """Given Party instance, when all defeated, then is_defeated returns True."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)
        party = Party([cloud, tifa])

        # When
        cloud.hp = 0
        tifa.hp = 0

        # Then
        assert party.is_defeated() is True
        assert party.is_alive() is False

    def test_given_party_when_get_defeated_members_then_returns_correct(self):
        """Given Party instance, when getting defeated members, then returns correct."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)
        aerith = Character(name="Aerith", job=Job.KNIGHT, hp=80, attack=18, intelligence=28, agility=18, speed=16, level=7)
        party = Party([cloud, tifa, aerith])

        # When
        cloud.hp = 0
        tifa.hp = 50

        # Then
        defeated = party.get_defeated_members()
        assert len(defeated) == 1
        assert cloud in defeated
        assert tifa not in defeated
        assert aerith not in defeated

    def test_given_party_when_calculating_total_hp_then_returns_sum(self):
        """Given Party instance, when calculating total HP, then returns sum."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)
        aerith = Character(name="Aerith", job=Job.KNIGHT, hp=80, attack=18, intelligence=28, agility=18, speed=16, level=7)
        party = Party([cloud, tifa, aerith])

        # When
        total_hp = party.get_total_hp()

        # Then
        assert total_hp == 270

    def test_given_party_when_some_defeated_then_total_hp_excludes_defeated(self):
        """Given Party instance, when some defeated, then total HP excludes defeated."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)
        party = Party([cloud, tifa])

        # When
        tifa.hp = 0
        total_hp = party.get_total_hp()

        # Then
        assert total_hp == 100

    def test_given_party_when_healing_all_then_hp_increases(self):
        """Given Party instance, when healing all, then HP increases."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=50, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=30, attack=28, intelligence=12, agility=22, speed=20, level=7)
        party = Party([cloud, tifa])

        # When
        total_healed = party.heal_all(20)

        # Then
        assert cloud.hp == 70
        assert tifa.hp == 50
        assert total_healed == 40

    def test_given_party_when_healing_defeated_member_then_not_healed(self):
        """Given Party instance, when healing, defeated members not healed."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=50, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=0, attack=28, intelligence=12, agility=22, speed=20, level=7)
        party = Party([cloud, tifa])

        # When
        total_healed = party.heal_all(20)

        # Then
        assert cloud.hp == 70
        assert tifa.hp == 0  # Still defeated
        assert total_healed == 20

    def test_given_party_when_iterating_then_yields_all_members(self):
        """Given Party instance, when iterating, then yields all members."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)
        party = Party([cloud, tifa])

        # When
        members_list = [m for m in party]

        # Then
        assert len(members_list) == 2
        assert cloud in members_list
        assert tifa in members_list

    def test_given_party_when_checking_contains_then_returns_correct(self):
        """Given Party instance, when checking contains, then returns correct."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)
        sep = Character(name="Sephiroth", job=Job.WARRIOR, hp=150, attack=35, intelligence=25, agility=25, speed=23, level=10)
        party = Party([cloud, tifa])

        # Then
        assert cloud in party
        assert tifa in party
        assert sep not in party

    def test_given_party_when_repr_then_shows_correct_format(self):
        """Given Party instance, when getting repr, then shows correct format."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)
        party = Party([cloud, tifa])

        # When
        result = repr(party)

        # Then
        assert result == "Party(members=2, alive=2)"

    def test_given_party_when_one_defeated_then_repr_shows_correct_alive_count(self):
        """Given Party instance, when one defeated, then repr shows correct alive count."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=0, attack=28, intelligence=12, agility=22, speed=20, level=7)
        party = Party([cloud, tifa])

        # When
        result = repr(party)

        # Then
        assert result == "Party(members=2, alive=1)"


class TestPartyWithUnits:
    """Tests for Party class with Unit instances (enemy groups)."""

    def test_given_enemy_party_when_creating_with_units_then_works_correctly(self):
        """Given Party with Units, when creating, then works correctly."""
        # Given
        goblin = Unit(type=UnitType.GOBLIN, hp=40, attack=15, intelligence=8, agility=20, speed=15, level=4)
        orc = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)
        slime = Unit(type=UnitType.SLIME, hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)

        # When
        enemy_party = Party([goblin, orc, slime])

        # Then
        assert len(enemy_party.members) == 3
        assert enemy_party.is_alive() is True
        assert goblin in enemy_party
        assert orc in enemy_party
        assert slime in enemy_party

    def test_given_enemy_party_when_members_defeated_then_is_defeated_works(self):
        """Given Party with Units, when members defeated, then is_defeated works."""
        # Given
        goblin = Unit(type=UnitType.GOBLIN, hp=40, attack=15, intelligence=8, agility=20, speed=15, level=4)
        orc = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)
        enemy_party = Party([goblin, orc])

        # When
        goblin.hp = 0
        orc.hp = 0

        # Then
        assert enemy_party.is_defeated() is True
        assert len(enemy_party.get_alive_members()) == 0

    def test_given_mixed_party_when_creating_then_works(self):
        """Given Party with mixed Characters and Units, when creating, then works."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        goblin = Unit(type=UnitType.GOBLIN, hp=40, attack=15, intelligence=8, agility=20, speed=15, level=4)

        # When
        mixed_party = Party([cloud, goblin])

        # Then
        assert len(mixed_party.members) == 2
        assert mixed_party.is_alive() is True
