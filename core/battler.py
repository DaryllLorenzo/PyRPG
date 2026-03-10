from abc import ABC
from dataclasses import dataclass

@dataclass
class Battler(ABC):
    """
    Abstract base class for all combat participants.

    This class defines the core attributes that any entity participating in
    battle must have, including both playable characters and enemies.

    Args:
        hp: Current health points
        attack: Physical attack power
        intelligence: Magical power affecting spells and healing
        agility: Speed and precision affecting turn order and evasion
        speed: Movement speed, useful for positioning systems
        level: Current level determining progression and available skills
    """
    
    hp: int
    attack: int
    intelligence: int
    agility: int
    speed: int
    level: int