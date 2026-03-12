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
| `core/items/item.py` | Equippable items with stats |
| `core/combat/battle_action.py` | Battle action dataclass |

**Missing:**

| File | Description |
|------|-------------|
| `core/combat/battle_system.py` | Main combat loop |
| `core/combat/damage_calculator.py` | Damage formulas |
| `core/combat/status_effect.py` | Status effects (Poison, Sleep, etc.) |
| `core/entities/party.py` | Player party management |
| `core/entities/enemy_party.py` | Enemy group management |
| `core/progression/skill.py` | Skills and abilities |
| `core/progression/experience.py` | XP and leveling system |
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

### Phase 2: Progression System (Priority: Medium)

1. Implement `skill.py` - skills and abilities
2. Implement `experience.py` - XP, level up
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

cloud = Character(name="Cloud", job=Job.WARRIOR, hp=100, attack=25, intelligence=15, agility=20, speed=18, level=7)

battle = BattleSystem(party, enemies)
battle.start()
```

## Requirements

- Python 3.14.2
- See `pyproject.toml` for dependencies
