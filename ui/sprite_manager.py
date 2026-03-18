"""
Sprite Manager for PyRPG.

Handles loading and splitting sprite sheets into individual animation frames.
"""

import pygame
from pathlib import Path
from typing import Dict, List


class SpriteManager:
    """Manages sprite sheet loading and animation frame extraction."""

    def __init__(self, tile_width: int = 140, tile_height: int = 155):
        """
        Initialize the SpriteManager.

        Args:
            tile_width: Width of each frame in pixels.
            tile_height: Height of each frame in pixels.
        """
        self.tile_width = tile_width
        self.tile_height = tile_height
        self._sprite_sheets: Dict[str, Dict[str, List[pygame.Surface]]] = {}

    def load_sprite_sheet(self, path: str, name: str) -> Dict[str, List[pygame.Surface]]:
        """
        Load a sprite sheet and split it into animation frames.

        The sprite sheet should have 4 rows (up, right, down, left)
        and multiple columns for animation frames.

        Args:
            path: Path to the sprite sheet image.
            name: Identifier name for this sprite sheet.

        Returns:
            Dictionary with directions as keys and list of frames as values.
        """
        image_path = Path(path)
        if not image_path.exists():
            raise FileNotFoundError(f"Sprite sheet not found: {path}")

        sheet = pygame.image.load(str(image_path)).convert_alpha()

        animations: Dict[str, List[pygame.Surface]] = {
            "up": [],
            "right": [],
            "down": [],
            "left": [],
        }

        rows = sheet.get_height() // self.tile_height
        cols = sheet.get_width() // self.tile_width

        for row in range(rows):
            for col in range(cols):
                # Extract frame from sprite sheet
                rect = pygame.Rect(
                    col * self.tile_width,
                    row * self.tile_height,
                    self.tile_width,
                    self.tile_height,
                )
                frame = pygame.Surface((self.tile_width, self.tile_height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), rect)

                # Assign to direction based on row
                if row == 0:
                    animations["up"].append(frame)
                elif row == 1:
                    animations["right"].append(frame)
                elif row == 2:
                    animations["down"].append(frame)
                elif row == 3:
                    animations["left"].append(frame)

        self._sprite_sheets[name] = animations
        return animations

    def get_animations(self, name: str) -> Dict[str, List[pygame.Surface]]:
        """
        Get previously loaded animations by name.

        Args:
            name: Identifier name of the loaded sprite sheet.

        Returns:
            Dictionary with directions and their animation frames.
        """
        if name not in self._sprite_sheets:
            raise KeyError(f"Sprite sheet '{name}' not loaded. Call load_sprite_sheet first.")
        return self._sprite_sheets[name]
