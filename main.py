"""
PyRPG - Main Entry Point

A turn-based JRPG with Pygame UI.
"""

import pygame
from pathlib import Path

from ui.sprite_manager import SpriteManager
from ui.player import Player
from ui.npc import NPC
from ui.collision import resolve_collision
from ui.tilemap import TileMap
from ui.triggers import TriggerZone, TriggerManager
from ui.camera import Camera
from ui.dialog_box import DialogBox


# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

# Map settings (PixelCrawler native tile size: 16x16)
TILE_SIZE = 16
MAP_WIDTH = 80  # tiles (1280 pixels - larger than screen for camera scrolling)
MAP_HEIGHT = 60  # tiles (960 pixels - larger than screen for camera scrolling)


def main():
    """Main game loop."""
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("PyRPG")

    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Load sprite sheets from PixelCrawler pack
    assets_dir = Path(__file__).parent / "ui" / "assets" / "PixelCrawler"
    sprite_manager = SpriteManager()

    # Load Body_A animations (64x64 tiles)
    idle = sprite_manager.load_body_a_animation(
        str(assets_dir), "Idle_Base", "idle"
    )
    walk = sprite_manager.load_body_a_animation(
        str(assets_dir), "Walk_Base", "walk"
    )
    run = sprite_manager.load_body_a_animation(
        str(assets_dir), "Run_Base", "run"
    )

    # Create tilemap for floor rendering
    tilemap = TileMap(tile_size=TILE_SIZE, map_width=MAP_WIDTH, map_height=MAP_HEIGHT)

    # Generate basic grass tile programmatically (avoids tileset clipping conflicts)
    grass_tile = tilemap.generate_basic_tile("grass", variation=0)
    tilemap.tiles[0] = grass_tile
    print("Generated basic grass tile for floor rendering")

    # Fill the entire map with grass tile (tile_id=0)
    tilemap.fill_all(0)

    # Create camera for scrolling
    camera = Camera(
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        map_width=tilemap.pixel_width,
        map_height=tilemap.pixel_height,
    )

    # Create player (starting near center of map)
    sprite_scale = 2
    player_start_x = tilemap.pixel_width // 2 - (64 * sprite_scale) // 2
    player_start_y = tilemap.pixel_height // 2 - (64 * sprite_scale) // 2
    player = Player(
        x=player_start_x,
        y=player_start_y,
        idle_animations=idle,
        walk_animations=walk,
        run_animations=run,
        walk_speed=3,
        run_speed=6,
        animation_speed=0.15,
        scale=sprite_scale,
        hitbox_width=32,
        hitbox_height=48,
        hitbox_offset_x=16,  # Center the hitbox
        hitbox_offset_y=16,
    )

    # Set camera to follow player instantly (Pokémon-style: player always centered)
    camera.set_smoothing(0.0)  # Instant follow, no delay
    camera.set_target(player)

    # Force camera to center on player at start
    camera.update()

    # Create NPC (static, same sprite as player)
    npc_x = player_start_x + 150
    npc_y = player_start_y
    npc = NPC(
        x=npc_x,
        y=npc_y,
        idle_animations=idle,
        walk_animations=walk,
        animation_speed=0.15,
        scale=sprite_scale,
        hitbox_width=32,
        hitbox_height=48,
        hitbox_offset_x=16,
        hitbox_offset_y=16,
        portrait_path=str(Path(__file__).parent / "ui" / "assets" / "elvigio_molesto.png"),
        dialog_text="¡Oye tú! Sí, tú mismo. ¿Qué haces por aquí? Este no es lugar para andar merodeando sin rumbo. ¡Más te vale tener un buen motivo para estar en estas tierras!",
        interaction_distance=100,
    )

    # Create trigger zones (replicating Unity's OnTriggerEnter2D)
    trigger_manager = TriggerManager()

    # Trigger zone 1: Near the starting area
    trigger1 = TriggerZone(
        x=player_start_x - 50,
        y=player_start_y - 50,
        width=100,
        height=100,
        trigger_id="start_area",
    )
    trigger1.on_enter = lambda entity_id: print(
        f"[TRIGGER ENTER] start_area - Entity {entity_id} entered the starting area!"
    )
    trigger1.on_exit = lambda entity_id: print(
        f"[TRIGGER EXIT] start_area - Entity {entity_id} left the starting area!"
    )
    trigger_manager.add_trigger(trigger1)

    # Trigger zone 2: Near the NPC
    trigger2 = TriggerZone(
        x=npc_x - 40,
        y=npc_y - 40,
        width=80,
        height=80,
        trigger_id="npc_zone",
    )
    trigger2.on_enter = lambda entity_id: print(
        f"[TRIGGER ENTER] npc_zone - Entity {entity_id} approached the NPC!"
    )
    trigger2.on_exit = lambda entity_id: print(
        f"[TRIGGER EXIT] npc_zone - Entity {entity_id} moved away from the NPC!"
    )
    trigger_manager.add_trigger(trigger2)

    # Trigger zone 3: One-shot trigger (fires only once)
    trigger3 = TriggerZone(
        x=player_start_x + 200,
        y=player_start_y,
        width=64,
        height=64,
        trigger_id="one_shot_event",
        one_shot=True,
    )
    trigger3.on_enter = lambda entity_id: print(
        f"[TRIGGER ENTER] one_shot_event - Entity {entity_id} triggered a one-time event!"
    )
    trigger_manager.add_trigger(trigger3)

    # Debug: Show trigger zones
    show_triggers = True

    # Create dialog box
    dialog_box = DialogBox(
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        portrait_scale=3,
        animation_speed=0.2,
    )

    # Dialog state
    dialog_active = False
    can_open_dialog = False

    # Game loop
    running = True
    while running:
        # Calculate delta time in milliseconds
        dt = clock.get_time()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_t:
                    # Toggle trigger visualization
                    show_triggers = not show_triggers
                    print(f"Trigger visualization: {'ON' if show_triggers else 'OFF'}")
                elif event.key == pygame.K_q and can_open_dialog and not dialog_active:
                    # Open dialog with NPC
                    dialog_active = True
                    portrait = npc.get_portrait()
                    if portrait:
                        dialog_box.load_portrait(str(Path(__file__).parent / "ui" / "assets" / "elvigio_molesto.png"))
                    dialog_box.set_text(npc.dialog_text)
                    dialog_box.open()
                    # Make NPC face player
                    npc.face_player(player.x, player.y)
                elif event.key == pygame.K_SPACE and dialog_active:
                    # Advance or close dialog
                    if not dialog_box.advance_text():
                        # Text complete, close dialog
                        dialog_box.close()
                        dialog_active = False

        # Update dialog box
        if dialog_active:
            dialog_box.update(dt)

        # Get input
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # Only allow movement when dialog is not active
        if not dialog_active:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -1
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 1

            # Check for running (Shift key)
            player.set_running(keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])

            # Update player with collision detection
            blocked_x, blocked_y = resolve_collision(player, npc, dx, dy)
            player.try_move(dx, dy, blocked_x, blocked_y)

            # Update camera to follow player
            camera.update()

        # Check if player can interact with NPC
        player_rect = player.get_rect()
        can_open_dialog = npc.can_interact(player.x, player.y, player_rect) and not dialog_active

        # Check trigger zones
        trigger_manager.update_all(player_rect, id(player))

        # Draw
        screen.fill((50, 50, 100))  # Dark blue background (fallback)

        # Draw tilemap (floor)
        tilemap.draw(screen, camera_x=camera.x, camera_y=camera.y)

        # Draw trigger zones (debug visualization)
        if show_triggers:
            trigger_manager.draw_all(
                screen,
                color=(255, 0, 0, 128),
                width=2,
                camera_x=camera.x,
                camera_y=camera.y,
            )

        # Draw entities sorted by Y position (bottom-first for correct overlap)
        # Convert entity positions to screen coordinates for drawing
        entities = []
        for entity in [player, npc]:
            screen_x, screen_y = camera.world_to_screen(entity.x, entity.y)
            entities.append((screen_y, entity, screen_x, screen_y))

        entities.sort(key=lambda e: e[0])
        for _, entity, draw_x, draw_y in entities:
            entity.draw(screen, draw_x=draw_x, draw_y=draw_y)

        # Draw dialog box (on top of everything)
        if dialog_active or not dialog_box.is_closed():
            dialog_box.update(dt)
            dialog_box.draw(screen)

        # Draw instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "Arrow keys or WASD to move",
            "Shift to run",
            "T: Toggle trigger visualization",
            "Q: Talk to NPC (when close)",
            "SPACE: Advance/close dialog",
            "ESC to quit",
        ]
        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (10, 10 + i * 20))

        # Draw interaction prompt
        if can_open_dialog and not dialog_active:
            prompt_text = "Press Q to talk"
            prompt_surface = font.render(prompt_text, True, (255, 255, 100))
            # Position above NPC
            npc_screen_x, npc_screen_y = camera.world_to_screen(npc.x, npc.y)
            prompt_x = npc_screen_x + (npc.get_rect().width // 2) - (prompt_surface.get_width() // 2)
            prompt_y = npc_screen_y - 30
            screen.blit(prompt_surface, (prompt_x, prompt_y))

        # Draw player position info
        pos_text = f"Position: ({player.x}, {player.y})"
        pos_surface = font.render(pos_text, True, (200, 200, 200))
        screen.blit(pos_surface, (10, SCREEN_HEIGHT - 30))

        # Draw map info
        map_text = f"Map: {MAP_WIDTH}x{MAP_HEIGHT} tiles ({tilemap.pixel_width}x{tilemap.pixel_height} px)"
        map_surface = font.render(map_text, True, (200, 200, 200))
        screen.blit(map_surface, (10, SCREEN_HEIGHT - 50))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
