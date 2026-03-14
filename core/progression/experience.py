from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Experience:
    """
    Manages experience points and leveling for a character.

    This class handles XP accumulation, level progression, and stat growth
    when leveling up. Uses a configurable experience curve and stat growth
    function to support different progression systems.

    Attributes:
        current_xp: Current experience points accumulated
        level: Current character level
        xp_curve: Function that calculates XP needed for next level
        stat_growth: Function that calculates stat increases on level up
        skills: List of skills learned at current level

    Example:
        >>> def simple_xp_curve(level: int) -> int:
        ...     return level * 100
        >>> def warrior_stat_growth(level: int) -> dict:
        ...     return {"hp": 10, "attack": 3, "intelligence": 1, "agility": 2, "speed": 2}
        >>> exp = Experience(current_xp=0, level=1, xp_curve=simple_xp_curve, stat_growth=warrior_stat_growth)
        >>> _ = exp.add_xp(150)
        >>> print(f"Level: {exp.level}, XP: {exp.current_xp}")
        Level: 2, XP: 50
        >>> print(f"Stats gained: {exp.last_level_up_stats}")
        Stats gained: {'hp': 10, 'attack': 3, 'intelligence': 1, 'agility': 2, 'speed': 2}

    See Also:
        - Character: Class that contains Experience component
        - Skill: Class representing learnable abilities
    """

    current_xp: int = 0
    level: int = 1
    xp_curve: Callable[[int], int] = field(default_factory=lambda: lambda level: level * 100)
    stat_growth: Callable[[int], dict] = field(default_factory=lambda: lambda level: {
        "hp": 5,
        "attack": 2,
        "intelligence": 1,
        "agility": 1,
        "speed": 1
    })
    skills: list = field(default_factory=list)
    last_level_up_stats: dict = field(default_factory=dict)
    _pending_level_ups: int = field(default=0, init=False, repr=False)

    def add_xp(self, amount: int) -> int:
        """
        Add experience points and handle level ups.

        Adds the specified amount of XP and checks if the character levels up.
        If enough XP is gained for multiple level ups, all are processed.
        Excess XP carries over to the next level.

        Args:
            amount: The amount of XP to add (must be positive)

        Returns:
            The number of levels gained from this XP addition

        Example:
            >>> exp = Experience(current_xp=80, level=1, xp_curve=lambda lvl: 100)
            >>> levels_gained = exp.add_xp(150)
            >>> print(f"Leveled up {levels_gained} time(s)")
            Leveled up 2 time(s)
        """
        if amount < 0:
            raise ValueError("XP amount must be positive")

        self.current_xp += amount
        self._pending_level_ups = 0

        while self.current_xp >= self.xp_to_next_level():
            self.current_xp -= self.xp_to_next_level()
            self._pending_level_ups += 1

        levels_gained = self._pending_level_ups
        
        if self._pending_level_ups > 0:
            self._do_level_up()

        return levels_gained

    def _do_level_up(self) -> None:
        """
        Process all pending level ups.

        Increases the character's level by the number of pending level ups
        and calculates the total stat gains. Skills are learned if the
        character reaches their required level.

        Note:
            This method is called automatically by add_xp() when leveling up.
            Stat gains are cumulative for multiple level ups.
        """
        old_level = self.level
        self.level += self._pending_level_ups

        total_stats = {
            "hp": 0,
            "attack": 0,
            "intelligence": 0,
            "agility": 0,
            "speed": 0
        }

        for lvl in range(old_level + 1, self.level + 1):
            stats = self.stat_growth(lvl)
            for stat, value in stats.items():
                total_stats[stat] += value

        self.last_level_up_stats = total_stats
        self._pending_level_ups = 0

    def xp_to_next_level(self) -> int:
        """
        Calculate the XP required to reach the next level.

        Uses the xp_curve function to determine how much XP is needed
        to advance from the current level.

        Returns:
            The amount of XP needed to reach the next level

        Example:
            >>> def simple_curve(level: int) -> int:
            ...     return level * 100
            >>> exp = Experience(level=1, xp_curve=simple_curve)
            >>> print(f"XP needed: {exp.xp_to_next_level()}")
            XP needed: 100
            >>> exp.level = 5
            >>> print(f"XP needed: {exp.xp_to_next_level()}")
            XP needed: 500
        """
        return self.xp_curve(self.level)

    def xp_progress(self) -> float:
        """
        Calculate the current XP progress as a percentage.

        Returns a value between 0.0 and 1.0 representing how close
        the character is to reaching the next level.

        Returns:
            Progress percentage (0.0 to 1.0)

        Example:
            >>> def simple_curve(level: int) -> int:
            ...     return 100
            >>> exp = Experience(current_xp=75, level=1, xp_curve=simple_curve)
            >>> print(f"Progress: {exp.xp_progress() * 100}%")
            Progress: 75.0%
        """
        xp_needed = self.xp_to_next_level()
        if xp_needed == 0:
            return 1.0
        return min(1.0, self.current_xp / xp_needed)

    def can_learn_skill(self, skill_level: int) -> bool:
        """
        Check if the character can learn a skill at their current level.

        Args:
            skill_level: The level at which the skill becomes available

        Returns:
            True if the character's level is >= the skill's required level

        Example:
            >>> exp = Experience(level=5)
            >>> print(exp.can_learn_skill(3))
            True
            >>> print(exp.can_learn_skill(7))
            False
        """
        return self.level >= skill_level

    def learn_skill(self, skill: "Skill", skill_level: int) -> bool:
        """
        Attempt to learn a new skill.

        Adds the skill to the character's known skills if they meet
        the level requirement and don't already know it.

        Args:
            skill: The Skill object to learn
            skill_level: The level at which this skill is learned

        Returns:
            True if the skill was learned, False if already known or
            level requirement not met

        Example:
            >>> from core.progression.skill import Skill
            >>> from core.enums.skill_type import SkillType
            >>> exp = Experience(level=3)
            >>> fire = Skill(name="Fire", description="Basic fire magic", type=SkillType.MAGIC, mp_cost=5, power=1.2)
            >>> learned = exp.learn_skill(fire, skill_level=2)
            >>> print(f"Skill learned: {learned}")
            Skill learned: True
        """
        if not self.can_learn_skill(skill_level):
            return False

        if any(s.name == skill.name for s in self.skills):
            return False

        self.skills.append(skill)
        return True


def linear_xp_curve(base: int = 100) -> Callable[[int], int]:
    """
    Create a linear XP curve function.

    Creates a function that returns XP requirements that scale linearly
    with level. Formula: XP = base * level

    Args:
        base: The base XP required for level 1 (default: 100)

    Returns:
        A function that takes a level and returns the XP needed

    Example:
        >>> xp_func = linear_xp_curve(100)
        >>> print(xp_func(1))
        100
        >>> print(xp_func(5))
        500
    """
    return lambda level: base * level


def exponential_xp_curve(base: int = 100, exponent: float = 1.5) -> Callable[[int], int]:
    """
    Create an exponential XP curve function.

    Creates a function that returns XP requirements that scale exponentially
    with level. Formula: XP = base * (level ^ exponent)

    Args:
        base: The base XP multiplier (default: 100)
        exponent: The growth exponent (default: 1.5)

    Returns:
        A function that takes a level and returns the XP needed

    Example:
        >>> xp_func = exponential_xp_curve(100, 1.5)
        >>> print(xp_func(1))
        100
        >>> print(xp_func(4))
        800
    """
    return lambda level: int(base * (level ** exponent))


def warrior_stat_growth(level: int) -> dict:
    """
    Stat growth function for warrior-type characters.

    Warriors gain high HP and attack, with moderate agility and speed,
    and low intelligence.

    Args:
        level: The level being gained (used for scaling)

    Returns:
        Dictionary of stat gains

    Example:
        >>> stats = warrior_stat_growth(5)
        >>> print(f"HP gain: +{stats['hp']}")
        HP gain: +13
    """
    return {
        "hp": 8 + level,
        "attack": 3 + (level // 3),
        "intelligence": 1,
        "agility": 2,
        "speed": 2
    }


def mage_stat_growth(level: int) -> dict:
    """
    Stat growth function for mage-type characters.

    Mages gain high intelligence and moderate HP, with lower physical stats.

    Args:
        level: The level being gained (used for scaling)

    Returns:
        Dictionary of stat gains

    Example:
        >>> stats = mage_stat_growth(5)
        >>> print(f"INT gain: +{stats['intelligence']}")
        INT gain: +9
    """
    return {
        "hp": 5 + (level // 2),
        "attack": 1,
        "intelligence": 4 + level,
        "agility": 1 + (level // 5),
        "speed": 2
    }


def thief_stat_growth(level: int) -> dict:
    """
    Stat growth function for thief-type characters.

    Thieves gain high agility and speed, with moderate HP and attack.

    Args:
        level: The level being gained (used for scaling)

    Returns:
        Dictionary of stat gains

    Example:
        >>> stats = thief_stat_growth(5)
        >>> print(f"AGI gain: +{stats['agility']}")
        AGI gain: +4
    """
    return {
        "hp": 6 + (level // 2),
        "attack": 2 + (level // 4),
        "intelligence": 1,
        "agility": 3 + (level // 3),
        "speed": 3 + (level // 3)
    }


def monk_stat_growth(level: int) -> dict:
    """
    Stat growth function for monk-type characters.

    Monks gain balanced stats with focus on HP, attack, and agility.

    Args:
        level: The level being gained (used for scaling)

    Returns:
        Dictionary of stat gains

    Example:
        >>> stats = monk_stat_growth(5)
        >>> print(f"HP gain: +{stats['hp']}, ATK gain: +{stats['attack']}")
        HP gain: +12, ATK gain: +4
    """
    return {
        "hp": 7 + level,
        "attack": 3 + (level // 3),
        "intelligence": 1,
        "agility": 3 + (level // 4),
        "speed": 2 + (level // 5)
    }
