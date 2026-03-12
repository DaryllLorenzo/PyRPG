from enum import Enum

class Job(Enum):
    """
    Character professions with associated gameplay characteristics

    Example:
        >>> job = Job.WARRIOR
        >>> print(f"{job.value}")
        Warrior
    """
    
    WARRIOR = "Warrior"
    KNIGHT = "Knight"
    MONK = "Monk"
    THIEF = "Thief"