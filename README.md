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
| `core/items/inventory.py` | Inventory management |

### Tests

**Implemented:**

| File | Description |
|------|-------------|
| `tests/test_entities.py` | Tests for Battler, Character, Unit |
| `tests/test_combat.py` | Tests for BattleAction, DamageCalculator |
| `tests/test_party.py` | Tests for Party class |
| `tests/test_battle_flow.py` | Integration tests for complete battle flow |
| `tests/test_progression.py` | Tests for Skill, Experience |
| `tests/test_items.py` | Tests for Item class |
| `tests/test_enums.py` | Tests for enum types |

**Missing:**

| File | Description |
|------|-------------|
| `tests/test_status_effects.py` | Tests for status effect system |
| `tests/test_inventory.py` | Tests for inventory management |

### UI

Graphical UI using Pygame with animated character sprites.

**Implemented:**

| File | Description |
|------|-------------|
| `ui/player.py` | Player character with idle/walk/run animations |
| `ui/npc.py` | Non-player characters with idle animations |
| `ui/collision.py` | Collision detection and resolution utilities |
| `ui/sprite_manager.py` | Sprite sheet loading and frame extraction |
| `ui/camera.py` | Camera system for scrolling and following entities |
| `ui/tilemap.py` | Tile-based floor map rendering |
| `ui/triggers.py` | Trigger zones (Unity-style OnTriggerEnter2D) |

**Assets:**

Sprite assets from **PixelCrawler - Free Pack** by [Anokolisa](https://anokolisa.itch.io/free-pixel-art-asset-pack-topdown-tileset-rpg-16x16-sprites).

**Working with PixelCrawler Sprites:**

The PixelCrawler pack uses directional sprite sheets (separate files for each direction):
- `*_Up-Sheet.png` - Up direction
- `*_Down-Sheet.png` - Down direction
- `*_Side-Sheet.png` - Right direction (automatically flipped for left)

```python
from ui.sprite_manager import SpriteManager
from ui.player import Player
from ui.npc import NPC
from ui.collision import resolve_collision

# Initialize sprite manager
sprite_manager = SpriteManager()

# Load Body_A animations (64x64 tiles)
assets_dir = "ui/assets/PixelCrawler"
idle = sprite_manager.load_body_a_animation(assets_dir, "Idle_Base", "idle")
walk = sprite_manager.load_body_a_animation(assets_dir, "Walk_Base", "walk")
run = sprite_manager.load_body_a_animation(assets_dir, "Run_Base", "run")

# Create player with animations
player = Player(
    x=100, y=100,
    idle_animations=idle,
    walk_animations=walk,
    run_animations=run,
    walk_speed=2,
    run_speed=4,
    animation_speed=0.15,
    scale=2,  # Render scale (64*scale pixels)
    hitbox_width=32,   # Collision box width
    hitbox_height=48,  # Collision box height
)

# Toggle running with Shift key
player.set_running(True)  # or False for walking

# Create static NPC
npc = NPC(
    x=250, y=100,
    idle_animations=idle,
    walk_animations=walk,
    scale=2,
    hitbox_width=32,
    hitbox_height=48,
)

# In game loop - handle collision
dx, dy = 1, 0  # Input direction
blocked_x, blocked_y = resolve_collision(player, npc, dx, dy)
player.try_move(dx, dy, blocked_x, blocked_y)
```

**Available Body_A Animations:**
- `Idle_Base` - 4 frames (standing still)
- `Walk_Base` - 8 frames (walking)
- `Run_Base` - 6 frames (running)

**Other Character Bodies:** Check `Entities/Characters/` for additional base bodies.

**NPC/Mob Sprites:** The pack also includes pre-made NPCs (Knight, Wizard, Rogue) and Mobs (Orc Crew, Skeleton Crew) in `Entities/Npc's/` and `Entities/Mobs/`.

### UI Architecture

**Entity Classes (`Player`, `NPC`):**
- Each entity manages its own animations independently
- `get_rect()` returns collision box based on configured `hitbox_width`, `hitbox_height`, and offsets
- `draw()` renders the current animation frame at entity position

**Collision System:**
- `resolve_collision(player, npc, dx, dy)` - Returns `(blocked_x, blocked_y)` tuple
- `player.try_move(dx, dy, blocked_x, blocked_y)` - Applies movement with collision blocking
- Hitboxes are independent per entity (configure via constructor)

**Z-Ordering (Draw Order):**
- Entities should be sorted by Y position before drawing
- Entities with higher Y (lower on screen) draw on top
- Creates correct depth perception when characters overlap

```python
# Example: Draw multiple entities with correct Z-order
entities = [player, npc1, npc2]
entities.sort(key=lambda e: e.y)  # Sort by Y position
for entity in entities:
    entity.draw(screen)
```

### Camera System

The camera follows the player Pokémon-style (always centered):

```python
from ui.camera import Camera

# Create camera
camera = Camera(
    screen_width=640,
    screen_height=480,
    map_width=1280,  # Must be larger than screen for scrolling
    map_height=960,
)

# Set camera to follow player instantly
camera.set_smoothing(0.0)  # 0.0 = instant, 1.0 = no movement
camera.set_target(player)

# In game loop
camera.update()  # Updates camera position to follow target

# Convert world coordinates to screen coordinates for drawing
screen_x, screen_y = camera.world_to_screen(entity.x, entity.y)
entity.draw(screen, draw_x=screen_x, draw_y=screen_y)
```

**Camera Features:**
- Instant or smoothed following (configurable)
- Dead zone support (area where camera doesn't move)
- Automatic clamping to map bounds
- World-to-screen and screen-to-world conversion

### TileMap System

Generate procedural floor tiles or load from tilesets:

```python
from ui.tilemap import TileMap

# Create tilemap
tilemap = TileMap(tile_size=16, map_width=80, map_height=60)

# Option 1: Generate procedural tiles (no conflicts)
grass_tile = tilemap.generate_basic_tile("grass", variation=0)
tilemap.tiles[0] = grass_tile
tilemap.fill_all(0)

# Option 2: Load from tileset image
tilemap.load_tileset("path/to/tileset.png", tile_id_start=0)

# Draw with camera scrolling
tilemap.draw(screen, camera_x=camera.x, camera_y=camera.y)
```

**Procedural Tile Types:**
- `grass` - Green with blade details
- `dirt` - Brown with pebbles
- `stone` - Gray with texture lines
- `sand` - Yellow with grain details

### Trigger Zones

Unity-style trigger zones for events and cutscenes:

```python
from ui.triggers import TriggerZone, TriggerManager

trigger_manager = TriggerManager()

# Create trigger zone
trigger = TriggerZone(
    x=100, y=100,
    width=64, height=64,
    trigger_id="battle_zone",
    one_shot=False,  # Set True for one-time events
)

# Set callbacks
trigger.on_enter = lambda entity_id: print(f"Entered by {entity_id}")
trigger.on_exit = lambda entity_id: print(f"Exited by {entity_id}")

trigger_manager.add_trigger(trigger)

# In game loop
trigger_manager.update_all(player.get_rect(), id(player))
```

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

1. ✓ Console-based UI (prototype)
2. ✓ Graphical UI with camera follow system
3. ✓ Procedural tile generation
4. ✓ Trigger zones for events

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
