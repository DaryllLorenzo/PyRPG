# PyRPG

Turn-based combat game inspired by classic JRPGs.

## Project Structure

```
PyRPG/
├── core/           # Game logic (no UI)
├── tests/          # Unit and integration tests
├── ui/             # Visual interface
└── main.py         # Entry point
```

## Current State

### Core Module

**Implemented:**

| File | Description |
|------|-------------|
| `core/entities/battler.py` | Abstract base class for combat participants |
| `core/entities/unit.py` | Generic enemies (mobs) |
| `core/entities/character.py` | Player characters with names and jobs |
| `core/enums/job.py` | Character classes (Warrior, Knight, Monk, Thief) |
| `core/enums/item_type.py` | Item categories (Sword, Pants, Helmet) |
| `core/enums/unit_type.py` | Enemy types (Slime, Orc, Goblin) |
| `core/enums/battle_action_type.py` | Action types (Attack, Skill, Item, Flee) |
| `core/enums/skill_type.py` | Skill categories (Physical, Magic, Support, Healing) |
| `core/items/item.py` | Equippable items with stats |
| `core/combat/battle_action.py` | Battle action dataclass |
| `core/combat/battle_result.py` | Result of a completed battle |
| `core/combat/battle_system.py` | Main combat loop |
| `core/combat/damage_calculator.py` | Damage formulas |
| `core/progression/skill.py` | Skills and abilities |
| `core/progression/experience.py` | XP and leveling system |

**Missing:**

| File | Description |
|------|-------------|
| `core/combat/status_effect.py` | Status effects (Poison, Sleep, etc.) |
| `core/entities/party.py` | Player party management |
| `core/entities/enemy_party.py` | Enemy group management |
| `core/items/inventory.py` | Inventory management |

### Tests

Empty. Pending implementation.

### UI

Empty. Pending implementation.

## Roadmap

### Phase 1: Core Combat System (Priority: High)

1. Implement `damage_calculator.py` - damage formulas
2. Implement `battle_system.py` - combat loop (1v1 then group)
3. Implement `party.py` and `enemy_party.py` - group combat
4. Implement `status_effect.py` - status effects

### Phase 2: Progression System (Priority: Medium) ✓

1. ✓ Implement `skill.py` - skills and abilities
2. ✓ Implement `experience.py` - XP, level up
3. Implement `inventory.py` - item management

### Phase 3: Testing (Priority: High)

1. Unit tests for all core modules
2. Integration tests for combat scenarios
3. Balance testing utilities

### Phase 4: UI (Priority: Low)

1. Console-based UI (prototype)
2. Graphical UI (optional)

## Usage

```python
# Example (pending implementation)
from core.entities import Character, Party
from core.combat import BattleSystem, BattleAction
from core.enums.job import Job
from core.progression import Experience, Skill
from core.enums.skill_type import SkillType
from core.progression.experience import warrior_stat_growth, exponential_xp_curve

# Create a character with experience system
cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)

# Set up experience system with warrior growth
cloud_exp = Experience(
    current_xp=0,
    level=7,
    xp_curve=exponential_xp_curve(100, 1.5),
    stat_growth=warrior_stat_growth
)

# Learn a skill
brave_slash = Skill(
    name="Brave Slash",
    description="A powerful slash dealing 150% damage",
    type=SkillType.PHYSICAL,
    mp_cost=5,
    power=1.5
)
cloud_exp.learn_skill(brave_slash, skill_level=5)

# Gain XP after battle
levels_gained = cloud_exp.add_xp(500)
print(f"Gained {levels_gained} level(s)!")

battle = BattleSystem(party, enemies)
battle.start()
```

## Requirements

- Python 3.14.2
- See `pyproject.toml` for dependencies
