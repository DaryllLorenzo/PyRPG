"""
PyRPG - Main Entry Point

A turn-based JRPG with Pygame UI.
"""

import pygame
from pathlib import Path

from ui.sprite_manager import SpriteManager
from ui.player import Player


# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60


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

    # Create player (centered on screen)
    sprite_scale = 2
    player_x = SCREEN_WIDTH // 2 - (64 * sprite_scale) // 2
    player_y = SCREEN_HEIGHT // 2 - (64 * sprite_scale) // 2
    player = Player(
        x=player_x,
        y=player_y,
        idle_animations=idle,
        walk_animations=walk,
        run_animations=run,
        walk_speed=2,
        run_speed=4,
        animation_speed=0.15,
        scale=sprite_scale,
    )

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Get input
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

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

        # Update player
        player.move(dx, dy)

        # Draw
        screen.fill((50, 50, 100))  # Dark blue background

        # Draw grid (optional, for visual reference)
        grid_size = 32
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(screen, (60, 60, 120), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(screen, (60, 60, 120), (0, y), (SCREEN_WIDTH, y))

        # Draw player
        player.draw(screen)

        # Draw instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "Arrow keys or WASD to move",
            "Shift to run",
            "ESC to quit",
        ]
        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (10, 10 + i * 20))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
