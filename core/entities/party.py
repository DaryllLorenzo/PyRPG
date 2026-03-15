from typing import List
from core.entities.battler import Battler


class Party:
    """
    Group of battlers fighting together.

    Manages a collection of combat participants, providing utilities
    for common party operations like checking alive members, adding
    or removing members, and checking party status.

    This class is generic and can be used for both player parties
    and enemy groups.

    Attributes:
        members: List of battlers in this party

    Example:
        >>> # Player party with characters
        >>> party = Party([cloud, tifa, aerith])
        >>> alive = party.get_alive_members()
        >>> print(f"{len(alive)} members ready to fight!")
        3 members ready to fight!

        >>> # Enemy party with units
        >>> enemies = Party([goblin, orc, slime])
        >>> if enemies.is_alive():
        ...     print("Enemies still fighting!")
        Enemies still fighting!

    Note:
        For player parties, use Character instances.
        For enemy groups, use Unit instances.
        Both work seamlessly since they inherit from Battler.

    See Also:
        - Battler: Base class for all combat participants
        - Character: Player-controlled party members
        - Unit: Enemy combat units
    """

    def __init__(self, members: List[Battler] = None):
        """
        Initialize a new party.

        Args:
            members: Optional list of initial party members.
                     If None, creates an empty party.

        Example:
            >>> party = Party([cloud, tifa])
            >>> empty_party = Party()
        """
        self.members: List[Battler] = members if members is not None else []

    def add_member(self, member: Battler) -> None:
        """
        Add a member to the party.

        Args:
            member: The battler to add to the party

        Example:
            >>> party = Party()
            >>> party.add_member(cloud)
            >>> print(f"Party size: {len(party.members)}")
            Party size: 1
        """
        self.members.append(member)

    def remove_member(self, member: Battler) -> bool:
        """
        Remove a member from the party.

        Args:
            member: The battler to remove from the party

        Returns:
            True if the member was removed, False if not found

        Example:
            >>> party = Party([cloud, tifa])
            >>> party.remove_member(cloud)
            True
            >>> len(party.members)
            1
        """
        if member in self.members:
            self.members.remove(member)
            return True
        return False

    def get_alive_members(self) -> List[Battler]:
        """
        Get all party members that are still alive.

        A member is considered alive if their HP is greater than 0.

        Returns:
            List of battlers with HP > 0

        Example:
            >>> cloud.hp = 100
            >>> tifa.hp = 0
            >>> party = Party([cloud, tifa])
            >>> alive = party.get_alive_members()
            >>> len(alive)
            1
            >>> alive[0].name
            'Cloud'
        """
        return [member for member in self.members if member.hp > 0]

    def get_defeated_members(self) -> List[Battler]:
        """
        Get all party members that have been defeated.

        A member is considered defeated if their HP is 0 or below.

        Returns:
            List of battlers with HP <= 0

        Example:
            >>> cloud.hp = 100
            >>> tifa.hp = 0
            >>> party = Party([cloud, tifa])
            >>> defeated = party.get_defeated_members()
            >>> len(defeated)
            1
            >>> defeated[0].name
            'Tifa'
        """
        return [member for member in self.members if member.hp <= 0]

    def is_alive(self) -> bool:
        """
        Check if the party still has any alive members.

        Returns:
            True if at least one member has HP > 0, False otherwise

        Example:
            >>> party = Party([cloud, tifa])
            >>> party.is_alive()
            True
            >>> cloud.hp = 0
            >>> tifa.hp = 0
            >>> party.is_alive()
            False
        """
        return len(self.get_alive_members()) > 0

    def is_defeated(self) -> bool:
        """
        Check if all party members have been defeated.

        Returns:
            True if all members have HP <= 0, False otherwise

        Example:
            >>> party = Party([cloud, tifa])
            >>> party.is_defeated()
            False
            >>> cloud.hp = 0
            >>> tifa.hp = 0
            >>> party.is_defeated()
            True
        """
        return not self.is_alive()

    def get_total_hp(self) -> int:
        """
        Get the sum of HP of all alive party members.

        Returns:
            Total HP of all alive members

        Example:
            >>> cloud.hp = 100
            >>> tifa.hp = 75
            >>> party = Party([cloud, tifa])
            >>> party.get_total_hp()
            175
        """
        return sum(member.hp for member in self.get_alive_members())

    def get_max_hp(self) -> int:
        """
        Get the sum of max HP potential (all members' current HP if fully healed).

        Note: This is a simple implementation. For proper max HP tracking,
        consider adding a max_hp attribute to Battler.

        Returns:
            Sum of current HP of all members (alive and defeated)

        Example:
            >>> cloud.hp = 50
            >>> tifa.hp = 30
            >>> party = Party([cloud, tifa])
            >>> party.get_max_hp()  # Returns current total, not potential max
            80
        """
        return sum(member.hp for member in self.members)

    def heal_all(self, amount: int) -> int:
        """
        Heal all alive party members by a specified amount.

        Each member is healed up to their current HP + amount.
        This method doesn't exceed any maximum HP limit (not tracked).

        Args:
            amount: Amount of HP to restore to each member

        Returns:
            Total HP restored across all members

        Example:
            >>> cloud.hp = 50
            >>> tifa.hp = 30
            >>> party = Party([cloud, tifa])
            >>> healed = party.heal_all(20)
            >>> cloud.hp
            70
            >>> tifa.hp
            50
            >>> healed
            40
        """
        total_healed = 0
        for member in self.get_alive_members():
            old_hp = member.hp
            member.hp += amount
            total_healed += member.hp - old_hp
        return total_healed

    def __len__(self) -> int:
        """
        Get the number of members in the party.

        Returns:
            Total number of party members (alive and defeated)

        Example:
            >>> party = Party([cloud, tifa, aerith])
            >>> len(party)
            3
        """
        return len(self.members)

    def __iter__(self):
        """
        Iterate over party members.

        Yields:
            Each battler in the party

        Example:
            >>> party = Party([cloud, tifa])
            >>> for member in party:
            ...     print(member.name)
            Cloud
            Tifa
        """
        return iter(self.members)

    def __contains__(self, member: Battler) -> bool:
        """
        Check if a battler is a member of the party.

        Args:
            member: The battler to check for membership

        Returns:
            True if the battler is in the party, False otherwise

        Example:
            >>> party = Party([cloud, tifa])
            >>> cloud in party
            True
            >>> sephiroth in party
            False
        """
        return member in self.members

    def __repr__(self) -> str:
        """
        Get a string representation of the party.

        Returns:
            String showing party size and alive member count

        Example:
            >>> party = Party([cloud, tifa])
            >>> repr(party)
            'Party(members=2, alive=2)'
        """
        alive_count = len(self.get_alive_members())
        return f"Party(members={len(self.members)}, alive={alive_count})"
