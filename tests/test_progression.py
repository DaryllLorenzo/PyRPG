"""
Tests for progression system classes in the game.

Tests verify the behavior of Skill and Experience classes.
"""

import pytest
from core.entities.character import Character
from core.enums.job import Job
from core.enums.skill_type import SkillType
from core.progression.skill import Skill
from core.progression.experience import (
    Experience,
    linear_xp_curve,
    exponential_xp_curve,
    warrior_stat_growth,
    mage_stat_growth,
    thief_stat_growth,
    monk_stat_growth
)


class TestSkill:
    """Tests for Skill class."""

    def test_given_skill_when_creating_physical_skill_then_has_correct_attributes(self):
        """Given Skill class, when creating physical skill, then has correct attributes."""
        # Given
        name = "Brave Slash"
        description = "A powerful slash that may inflict poison"
        skill_type = SkillType.PHYSICAL
        mp_cost = 5
        power = 1.5
        status_effect = "Poison"
        status_chance = 0.3

        # When
        skill = Skill(
            name=name,
            description=description,
            type=skill_type,
            mp_cost=mp_cost,
            power=power,
            status_effect=status_effect,
            status_chance=status_chance
        )

        # Then
        assert skill.name == name
        assert skill.description == description
        assert skill.type == skill_type
        assert skill.mp_cost == mp_cost
        assert skill.power == power
        assert skill.status_effect == status_effect
        assert skill.status_chance == status_chance

    def test_given_skill_when_creating_magic_skill_then_type_is_magic(self):
        """Given Skill, when creating magic skill, then type is MAGIC."""
        # Given
        expected_type = SkillType.MAGIC

        # When
        skill = Skill(
            name="Fire",
            description="Basic fire magic",
            type=SkillType.MAGIC,
            mp_cost=8,
            power=1.8
        )

        # Then
        assert skill.type == expected_type

    def test_given_skill_when_creating_healing_skill_then_type_is_healing(self):
        """Given Skill, when creating healing skill, then type is HEALING."""
        # Given
        expected_type = SkillType.HEALING

        # When
        skill = Skill(
            name="Cure",
            description="Restores HP to a target",
            type=SkillType.HEALING,
            mp_cost=10,
            power=1.0
        )

        # Then
        assert skill.type == expected_type

    def test_given_skill_when_creating_support_skill_then_type_is_support(self):
        """Given Skill, when creating support skill, then type is SUPPORT."""
        # Given
        expected_type = SkillType.SUPPORT

        # When
        skill = Skill(
            name="Haste",
            description="Increases target's speed",
            type=SkillType.SUPPORT,
            mp_cost=15,
            power=1.0,
            status_effect="Haste",
            status_chance=1.0
        )

        # Then
        assert skill.type == expected_type

    def test_given_skill_when_creating_without_status_effect_then_status_effect_is_none(self):
        """Given Skill, when creating without status effect, then status_effect is None."""
        # Given
        expected_status_effect = None

        # When
        skill = Skill(
            name="Power Strike",
            description="A powerful strike",
            type=SkillType.PHYSICAL,
            mp_cost=3,
            power=1.3
        )

        # Then
        assert skill.status_effect == expected_status_effect

    def test_given_skill_when_creating_without_status_chance_then_status_chance_is_zero(self):
        """Given Skill, when creating without status chance, then status_chance is 0.0."""
        # Given
        expected_status_chance = 0.0

        # When
        skill = Skill(
            name="Power Strike",
            description="A powerful strike",
            type=SkillType.PHYSICAL,
            mp_cost=3,
            power=1.3
        )

        # Then
        assert skill.status_chance == expected_status_chance

    def test_given_skill_when_creating_free_skill_then_mp_cost_is_zero(self):
        """Given Skill, when creating free skill, then mp_cost is 0."""
        # Given
        expected_mp_cost = 0

        # When
        skill = Skill(
            name="Basic Attack",
            description="A basic attack",
            type=SkillType.PHYSICAL,
            mp_cost=0,
            power=1.0
        )

        # Then
        assert skill.mp_cost == expected_mp_cost

    def test_given_two_skills_with_same_attributes_when_comparing_then_are_equal(self):
        """Given two skills with same attributes, when comparing, then are equal."""
        # Given
        skill1 = Skill(
            name="Fire",
            description="Basic fire magic",
            type=SkillType.MAGIC,
            mp_cost=8,
            power=1.8
        )
        skill2 = Skill(
            name="Fire",
            description="Basic fire magic",
            type=SkillType.MAGIC,
            mp_cost=8,
            power=1.8
        )

        # When
        result = skill1 == skill2

        # Then
        assert result is True

    def test_given_two_skills_with_different_names_when_comparing_then_are_not_equal(self):
        """Given two skills with different names, when comparing, then are not equal."""
        # Given
        skill1 = Skill(
            name="Fire",
            description="Basic fire magic",
            type=SkillType.MAGIC,
            mp_cost=8,
            power=1.8
        )
        skill2 = Skill(
            name="Blizzard",
            description="Basic ice magic",
            type=SkillType.MAGIC,
            mp_cost=8,
            power=1.8
        )

        # When
        result = skill1 == skill2

        # Then
        assert result is False


class TestExperience:
    """Tests for Experience class."""

    def test_given_experience_when_creating_then_starts_at_level_one(self):
        """Given Experience class, when creating, then starts at level 1."""
        # Given
        expected_level = 1

        # When
        exp = Experience()

        # Then
        assert exp.level == expected_level

    def test_given_experience_when_creating_then_starts_with_zero_xp(self):
        """Given Experience class, when creating, then starts with 0 XP."""
        # Given
        expected_xp = 0

        # When
        exp = Experience()

        # Then
        assert exp.current_xp == expected_xp

    def test_given_experience_when_adding_xp_below_threshold_then_level_does_not_change(self):
        """Given Experience, when adding XP below threshold, then level does not change."""
        # Given
        exp = Experience(current_xp=0, level=1, xp_curve=lambda lvl: 100)
        xp_to_add = 50
        expected_level = 1

        # When
        exp.add_xp(xp_to_add)

        # Then
        assert exp.level == expected_level
        assert exp.current_xp == xp_to_add

    def test_given_experience_when_adding_xp_reaching_threshold_then_level_increases(self):
        """Given Experience, when adding XP reaching threshold, then level increases."""
        # Given
        exp = Experience(current_xp=0, level=1, xp_curve=lambda lvl: 100)
        xp_to_add = 100
        expected_level = 2

        # When
        exp.add_xp(xp_to_add)

        # Then
        assert exp.level == expected_level
        assert exp.current_xp == 0

    def test_given_experience_when_adding_xp_exceeding_threshold_then_excess_carries_over(self):
        """Given Experience, when adding XP exceeding threshold, then excess carries over."""
        # Given
        exp = Experience(current_xp=0, level=1, xp_curve=lambda lvl: 100)
        xp_to_add = 150
        expected_level = 2
        expected_remaining_xp = 50

        # When
        exp.add_xp(xp_to_add)

        # Then
        assert exp.level == expected_level
        assert exp.current_xp == expected_remaining_xp

    def test_given_experience_when_adding_xp_for_multiple_level_ups_then_levels_increase_correctly(self):
        """Given Experience, when adding XP for multiple level ups, then levels increase correctly."""
        # Given
        exp = Experience(current_xp=0, level=1, xp_curve=lambda lvl: 100)
        xp_to_add = 350  # Enough for 3 level ups (100 + 200 + 50 remaining)
        expected_level = 4
        expected_remaining_xp = 50

        # When
        levels_gained = exp.add_xp(xp_to_add)

        # Then
        assert exp.level == expected_level
        assert exp.current_xp == expected_remaining_xp
        assert levels_gained == 3

    def test_given_experience_when_adding_negative_xp_then_raises_value_error(self):
        """Given Experience, when adding negative XP, then raises ValueError."""
        # Given
        exp = Experience()

        # When/Then
        with pytest.raises(ValueError):
            exp.add_xp(-50)

    def test_given_experience_when_checking_xp_to_next_level_then_returns_correct_value(self):
        """Given Experience, when checking XP to next level, then returns correct value."""
        # Given
        exp = Experience(level=1, xp_curve=lambda lvl: lvl * 100)
        expected_xp = 100

        # When
        result = exp.xp_to_next_level()

        # Then
        assert result == expected_xp

    def test_given_experience_when_checking_xp_to_next_level_at_higher_level_then_returns_higher_value(self):
        """Given Experience at higher level, when checking XP to next level, then returns higher value."""
        # Given
        exp = Experience(level=5, xp_curve=lambda lvl: lvl * 100)
        expected_xp = 500

        # When
        result = exp.xp_to_next_level()

        # Then
        assert result == expected_xp

    def test_given_experience_when_checking_xp_progress_then_returns_correct_percentage(self):
        """Given Experience, when checking XP progress, then returns correct percentage."""
        # Given
        exp = Experience(current_xp=50, level=1, xp_curve=lambda lvl: 100)
        expected_progress = 0.5

        # When
        result = exp.xp_progress()

        # Then
        assert result == expected_progress

    def test_given_experience_when_at_max_xp_then_progress_is_one(self):
        """Given Experience at max XP, when checking progress, then is 1.0."""
        # Given
        exp = Experience(current_xp=100, level=1, xp_curve=lambda lvl: 100)
        expected_progress = 1.0

        # When
        result = exp.xp_progress()

        # Then
        assert result == expected_progress

    def test_given_experience_when_checking_can_learn_skill_below_level_then_returns_false(self):
        """Given Experience, when checking can learn skill below level, then returns False."""
        # Given
        exp = Experience(level=3)
        skill_level = 5

        # When
        result = exp.can_learn_skill(skill_level)

        # Then
        assert result is False

    def test_given_experience_when_checking_can_learn_skill_at_level_then_returns_true(self):
        """Given Experience, when checking can learn skill at level, then returns True."""
        # Given
        exp = Experience(level=5)
        skill_level = 5

        # When
        result = exp.can_learn_skill(skill_level)

        # Then
        assert result is True

    def test_given_experience_when_checking_can_learn_skill_above_level_then_returns_true(self):
        """Given Experience, when checking can learn skill above level, then returns True."""
        # Given
        exp = Experience(level=7)
        skill_level = 3

        # When
        result = exp.can_learn_skill(skill_level)

        # Then
        assert result is True

    def test_given_experience_when_learning_skill_meeting_requirements_then_returns_true(self):
        """Given Experience meeting requirements, when learning skill, then returns True."""
        # Given
        exp = Experience(level=5)
        skill = Skill(name="Fire", description="Fire magic", type=SkillType.MAGIC, mp_cost=8, power=1.8)
        skill_level = 3

        # When
        result = exp.learn_skill(skill, skill_level)

        # Then
        assert result is True
        assert skill in exp.skills

    def test_given_experience_when_learning_skill_not_meeting_requirements_then_returns_false(self):
        """Given Experience not meeting requirements, when learning skill, then returns False."""
        # Given
        exp = Experience(level=2)
        skill = Skill(name="Fire", description="Fire magic", type=SkillType.MAGIC, mp_cost=8, power=1.8)
        skill_level = 5

        # When
        result = exp.learn_skill(skill, skill_level)

        # Then
        assert result is False
        assert skill not in exp.skills

    def test_given_experience_when_learning_same_skill_twice_then_second_returns_false(self):
        """Given Experience, when learning same skill twice, then second attempt returns False."""
        # Given
        exp = Experience(level=5)
        skill = Skill(name="Fire", description="Fire magic", type=SkillType.MAGIC, mp_cost=8, power=1.8)
        skill_level = 3

        # When
        exp.learn_skill(skill, skill_level)
        result = exp.learn_skill(skill, skill_level)

        # Then
        assert result is False

    def test_given_experience_when_leveling_up_then_last_level_up_stats_is_populated(self):
        """Given Experience, when leveling up, then last_level_up_stats is populated."""
        # Given
        exp = Experience(
            current_xp=0,
            level=1,
            xp_curve=lambda lvl: 100,
            stat_growth=lambda lvl: {"hp": 10, "attack": 3, "intelligence": 1, "agility": 2, "speed": 2}
        )

        # When
        exp.add_xp(150)

        # Then
        assert exp.last_level_up_stats is not None
        assert exp.last_level_up_stats["hp"] > 0

    def test_given_experience_with_linear_curve_when_leveling_then_xp_scales_linearly(self):
        """Given Experience with linear curve, when leveling, then XP scales linearly."""
        # Given
        exp = Experience(level=1, xp_curve=linear_xp_curve(100))

        # When
        xp_level_1 = exp.xp_to_next_level()
        exp.level = 5
        xp_level_5 = exp.xp_to_next_level()

        # Then
        assert xp_level_1 == 100
        assert xp_level_5 == 500

    def test_given_experience_with_exponential_curve_when_leveling_then_xp_scales_exponentially(self):
        """Given Experience with exponential curve, when leveling, then XP scales exponentially."""
        # Given
        exp = Experience(level=1, xp_curve=exponential_xp_curve(100, 1.5))

        # When
        xp_level_1 = exp.xp_to_next_level()
        exp.level = 4
        xp_level_4 = exp.xp_to_next_level()

        # Then
        assert xp_level_1 == 100
        assert xp_level_4 == 800  # 100 * 4^1.5 = 800


class TestStatGrowthFunctions:
    """Tests for stat growth functions."""

    def test_given_warrior_stat_growth_when_leveling_then_gains_high_hp_and_attack(self):
        """Given warrior stat growth, when leveling, then gains high HP and attack."""
        # Given
        level = 5

        # When
        stats = warrior_stat_growth(level)

        # Then
        assert stats["hp"] > stats["intelligence"]
        assert stats["attack"] > stats["intelligence"]

    def test_given_mage_stat_growth_when_leveling_then_gains_high_intelligence(self):
        """Given mage stat growth, when leveling, then gains high intelligence."""
        # Given
        level = 5

        # When
        stats = mage_stat_growth(level)

        # Then
        assert stats["intelligence"] > stats["attack"]
        assert stats["intelligence"] > stats["hp"]

    def test_given_thief_stat_growth_when_leveling_then_gains_high_agility_and_speed(self):
        """Given thief stat growth, when leveling, then gains high agility and speed."""
        # Given
        level = 5

        # When
        stats = thief_stat_growth(level)

        # Then
        assert stats["agility"] > stats["intelligence"]
        assert stats["speed"] > stats["intelligence"]

    def test_given_monk_stat_growth_when_leveling_then_gains_balanced_stats(self):
        """Given monk stat growth, when leveling, then gains balanced stats."""
        # Given
        level = 5

        # When
        stats = monk_stat_growth(level)

        # Then
        assert stats["hp"] > 0
        assert stats["attack"] > 0
        assert stats["agility"] > 0

    def test_given_stat_growth_function_when_higher_level_then_stats_increase(self):
        """Given stat growth function, when higher level, then stats increase."""
        # Given
        low_level = 1
        high_level = 10

        # When
        low_stats = warrior_stat_growth(low_level)
        high_stats = warrior_stat_growth(high_level)

        # Then
        assert high_stats["hp"] > low_stats["hp"]
        assert high_stats["attack"] > low_stats["attack"]
