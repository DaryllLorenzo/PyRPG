"""
Integration tests for complete battle flow.

Tests simulate full combat scenarios from start to finish,
verifying the interaction between all core combat systems.
"""

import pytest
from core.entities.character import Character
from core.entities.unit import Unit
from core.entities.party import Party
from core.combat.battle_system import BattleSystem
from core.combat.battle_result import BattleResult
from core.enums.job import Job
from core.enums.unit_type import UnitType


class TestBasicBattleFlow:
    """Tests for basic 1v1 battle scenarios."""

    def test_given_1v1_battle_when_stronger_character_fights_then_wins(self):
        """Given 1v1 battle with stronger character, when fighting, then wins."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        goblin = Unit(type=UnitType.GOBLIN, hp=40, attack=15, intelligence=8, agility=20, speed=15, level=3)

        party = Party([cloud])
        enemies = Party([goblin])

        battle = BattleSystem(party.members, enemies.members)

        # When
        result = battle.start()

        # Then
        assert result.won is True
        assert cloud.hp > 0  # Cloud survived
        assert goblin.hp <= 0  # Goblin defeated

    def test_given_1v1_battle_when_weaker_character_fights_then_loses(self):
        """Given 1v1 battle with weaker character, when fighting, then loses."""
        # Given
        weak_hero = Character(name="Weak Hero", job=Job.THIEF, hp=30, attack=5, intelligence=5, agility=10, speed=8, level=1)
        orc = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)

        party = Party([weak_hero])
        enemies = Party([orc])

        battle = BattleSystem(party.members, enemies.members)

        # When
        result = battle.start()

        # Then
        assert result.won is False
        assert weak_hero.hp <= 0  # Hero defeated
        assert orc.hp > 0  # Orc survived


class TestPartyBattleFlow:
    """Tests for party vs party battle scenarios."""

    def test_given_3v3_battle_when_party_has_advantage_then_wins(self):
        """Given 3v3 battle with advantaged party, when fighting, then wins."""
        # Given - Player party: higher level, better stats
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=120, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=100, attack=28, intelligence=12, agility=22, speed=20, level=7)
        aerith = Character(name="Aerith", job=Job.KNIGHT, hp=90, attack=18, intelligence=28, agility=18, speed=16, level=7)

        # Given - Enemy party: lower level, weaker stats
        goblin1 = Unit(type=UnitType.GOBLIN, hp=40, attack=15, intelligence=8, agility=20, speed=15, level=3)
        goblin2 = Unit(type=UnitType.GOBLIN, hp=40, attack=15, intelligence=8, agility=20, speed=15, level=3)
        slime = Unit(type=UnitType.SLIME, hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)

        player_party = Party([cloud, tifa, aerith])
        enemy_party = Party([goblin1, goblin2, slime])

        battle = BattleSystem(player_party.members, enemy_party.members)

        # When
        result = battle.start()

        # Then
        assert result.won is True
        assert len(result.survivors) > 0
        assert enemy_party.is_defeated() is True

    def test_given_3v3_battle_when_enemies_have_advantage_then_party_loses(self):
        """Given 3v3 battle with advantaged enemies, when fighting, then party loses."""
        # Given - Player party: low level, weak
        weak_hero1 = Character(name="Hero 1", job=Job.THIEF, hp=40, attack=10, intelligence=8, agility=15, speed=12, level=2)
        weak_hero2 = Character(name="Hero 2", job=Job.WARRIOR, hp=50, attack=12, intelligence=5, agility=10, speed=8, level=2)
        weak_hero3 = Character(name="Hero 3", job=Job.KNIGHT, hp=45, attack=10, intelligence=10, agility=12, speed=10, level=2)

        # Given - Enemy party: high level, strong
        orc1 = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)
        orc2 = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)
        orc3 = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)

        player_party = Party([weak_hero1, weak_hero2, weak_hero3])
        enemy_party = Party([orc1, orc2, orc3])

        battle = BattleSystem(player_party.members, enemy_party.members)

        # When
        result = battle.start()

        # Then
        assert result.won is False
        assert player_party.is_defeated() is True

    def test_given_balanced_battle_when_run_multiple_times_then_completes(self):
        """Given balanced battle, when run multiple times, then completes."""
        # Given - Balanced parties
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=20, intelligence=15, agility=20, speed=18, level=5)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=22, intelligence=12, agility=22, speed=20, level=5)

        orc = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)
        goblin = Unit(type=UnitType.GOBLIN, hp=40, attack=15, intelligence=8, agility=20, speed=15, level=4)

        player_party = Party([cloud, tifa])
        enemy_party = Party([orc, goblin])

        # When - Run battle 3 times
        results = []
        for _ in range(3):
            # Reset HP
            cloud.hp = 100
            tifa.hp = 90
            orc.hp = 80
            goblin.hp = 40

            battle = BattleSystem(player_party.members, enemy_party.members)
            result = battle.start()
            results.append(result)

        # Then - All battles completed (no infinite loops)
        assert len(results) == 3
        assert all(isinstance(r, BattleResult) for r in results)


class TestCompleteGameFlow:
    """Tests simulating a complete basic game session."""

    def test_given_complete_game_flow_when_playing_through_battles_then_completes(self):
        """
        Given complete game flow, when playing through multiple battles, then completes.

        Simulates:
        1. Create player party
        2. Fight first encounter (easy)
        3. Fight second encounter (medium)
        4. Fight boss encounter (hard)
        5. Verify victory condition
        """
        # Given - Player party (persistent through battles)
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=120, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=100, attack=28, intelligence=12, agility=22, speed=20, level=7)
        aerith = Character(name="Aerith", job=Job.KNIGHT, hp=90, attack=18, intelligence=28, agility=18, speed=16, level=7)

        player_party = Party([cloud, tifa, aerith])

        # Battle 1: Easy encounter (slimes)
        slime1 = Unit(type=UnitType.SLIME, hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)
        slime2 = Unit(type=UnitType.SLIME, hp=45, attack=12, intelligence=5, agility=15, speed=10, level=3)

        battle1 = BattleSystem(player_party.members, [slime1, slime2])
        result1 = battle1.start()

        # Verify first battle won
        assert result1.won is True

        # Battle 2: Medium encounter (goblins + orc)
        goblin = Unit(type=UnitType.GOBLIN, hp=40, attack=15, intelligence=8, agility=20, speed=15, level=4)
        orc = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)

        # Reset party HP partially (simulating no healing between battles)
        cloud.hp = max(1, cloud.hp)
        tifa.hp = max(1, tifa.hp)
        aerith.hp = max(1, aerith.hp)

        battle2 = BattleSystem(player_party.members, [goblin, orc])
        result2 = battle2.start()

        # Verify second battle won
        assert result2.won is True

        # Battle 3: Boss encounter (strong orc leader)
        orc_boss = Unit(type=UnitType.ORC, hp=150, attack=30, intelligence=10, agility=15, speed=12, level=8)
        orc_guard1 = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)
        orc_guard2 = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)

        # Party still has damage from previous battles
        battle3 = BattleSystem(player_party.members, [orc_boss, orc_guard1, orc_guard2])
        result3 = battle3.start()

        # Then - Complete game flow successful
        assert result3.won is True
        assert len(result3.survivors) >= 1  # At least one survivor

    def test_given_complete_game_flow_when_party_wipes_then_game_over(self):
        """
        Given complete game flow, when party is defeated, then game over.

        Simulates:
        1. Create weak player party
        2. Fight encounter too strong for them
        3. Verify game over condition
        """
        # Given - Weak player party
        rookie1 = Character(name="Rookie 1", job=Job.THIEF, hp=40, attack=10, intelligence=8, agility=15, speed=12, level=2)
        rookie2 = Character(name="Rookie 2", job=Job.WARRIOR, hp=50, attack=12, intelligence=5, agility=10, speed=8, level=2)

        player_party = Party([rookie1, rookie2])

        # Given - Strong enemy party (boss + guards)
        orc_boss = Unit(type=UnitType.ORC, hp=150, attack=30, intelligence=10, agility=15, speed=12, level=8)
        orc_guard1 = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)

        battle = BattleSystem(player_party.members, [orc_boss, orc_guard1])

        # When
        result = battle.start()

        # Then - Game over (party wiped)
        assert result.won is False
        assert len(result.survivors) == 0
        assert player_party.is_defeated() is True


class TestBattleSystemWithParty:
    """Tests for BattleSystem integration with Party class."""

    def test_given_battle_system_when_using_party_class_then_works(self):
        """Given BattleSystem with Party class, when battling, then works."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=90, attack=28, intelligence=12, agility=22, speed=20, level=7)

        goblin = Unit(type=UnitType.GOBLIN, hp=40, attack=15, intelligence=8, agility=20, speed=15, level=4)
        orc = Unit(type=UnitType.ORC, hp=80, attack=18, intelligence=5, agility=10, speed=8, level=5)

        player_party = Party([cloud, tifa])
        enemy_party = Party([goblin, orc])

        # When - Use Party.members for BattleSystem
        battle = BattleSystem(player_party.members, enemy_party.members)
        result = battle.start()

        # Then
        assert result.won is True
        assert player_party.is_alive() is True
        assert enemy_party.is_defeated() is True

    def test_given_battle_when_party_members_fall_then_survivors_tracked(self):
        """Given battle, when party members fall, then survivors tracked correctly."""
        # Given
        cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)
        tifa = Character(name="Tifa", job=Job.MONK, hp=50, attack=28, intelligence=12, agility=22, speed=20, level=7)  # Low HP
        aerith = Character(name="Aerith", job=Job.KNIGHT, hp=40, attack=18, intelligence=28, agility=18, speed=16, level=7)  # Low HP

        # Strong enemies to ensure party takes damage
        orc1 = Unit(type=UnitType.ORC, hp=100, attack=25, intelligence=5, agility=10, speed=8, level=6)
        orc2 = Unit(type=UnitType.ORC, hp=100, attack=25, intelligence=5, agility=10, speed=8, level=6)

        player_party = Party([cloud, tifa, aerith])
        enemy_party = Party([orc1, orc2])

        battle = BattleSystem(player_party.members, enemy_party.members)

        # When
        result = battle.start()

        # Then - Survivors correctly tracked
        assert result.won is True
        assert len(result.survivors) <= 3  # At most 3 survivors
        assert len(result.survivors) == len(player_party.get_alive_members())
