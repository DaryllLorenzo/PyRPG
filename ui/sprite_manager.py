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

        # Load image and convert to surface with alpha channel
        sheet = pygame.image.load(str(image_path))
        if sheet.get_alpha() is None:
            converted = pygame.Surface(sheet.get_size(), pygame.SRCALPHA)
            converted.blit(sheet, (0, 0))
            sheet = converted

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

    def load_directional_sprites(
        self, base_path: str, name: str, tile_width: int = 16, tile_height: int = 16
    ) -> Dict[str, List[pygame.Surface]]:
        """
        Load directional sprite sheets (separate files for Up, Down, Side).

        Expects files named:
        - *_Up-Sheet.png (or _Up.png)
        - *_Down-Sheet.png (or _Down.png)
        - *_Side-Sheet.png (or _Side.png)

        Side sprites are used for both right and left (left is flipped).

        Args:
            base_path: Base path without the direction suffix (e.g., 
                       "assets/PixelCrawler/Entities/Characters/Body_A/Animations/Run_Base/Run").
            name: Identifier name for this sprite sheet.
            tile_width: Width of each frame in pixels (default: 16).
            tile_height: Height of each frame in pixels (default: 16).

        Returns:
            Dictionary with directions as keys and list of frames as values.
        """
        base = Path(base_path)

        animations: Dict[str, List[pygame.Surface]] = {
            "up": [],
            "right": [],
            "down": [],
            "left": [],
        }

        direction_map = {
            "Up": "up",
            "Down": "down",
            "Side": "right",
        }

        for suffix, direction in direction_map.items():
            # Try both -Sheet.png and .png formats
            sheet_path = base.parent / f"{base.stem}_{suffix}-Sheet.png"
            if not sheet_path.exists():
                sheet_path = base.parent / f"{base.stem}_{suffix}.png"
            if not sheet_path.exists():
                continue

            sheet = pygame.image.load(str(sheet_path))
            # Convert to surface with alpha channel if needed
            if sheet.get_alpha() is None:
                converted = pygame.Surface(sheet.get_size(), pygame.SRCALPHA)
                converted.blit(sheet, (0, 0))
                sheet = converted

            # Auto-detect tile height from image (assume single row)
            detected_height = sheet.get_height()
            # Auto-detect tile width if not specified (assume square tiles)
            if tile_width == tile_height:
                detected_width = sheet.get_width() // (sheet.get_width() // tile_height)
                if detected_width == detected_height:
                    tile_width = detected_width
                    tile_height = detected_height

            cols = sheet.get_width() // tile_width

            for col in range(cols):
                rect = pygame.Rect(
                    col * tile_width,
                    0,
                    tile_width,
                    tile_height,
                )
                frame = sheet.subsurface(rect).copy()

                if direction == "right":
                    # Store original for right, flip for left
                    animations["right"].append(frame)
                    flipped = pygame.transform.flip(frame, True, False)
                    animations["left"].append(flipped)
                else:
                    animations[direction].append(frame)

        self._sprite_sheets[name] = animations
        return animations

    def load_body_a_animation(
        self,
        assets_dir: str,
        animation_type: str,
        name: str,
        tile_width: int = 64,
        tile_height: int = 64,
    ) -> Dict[str, List[pygame.Surface]]:
        """
        Load Body_A character animations from PixelCrawler pack.

        Args:
            assets_dir: Path to PixelCrawler assets directory.
            animation_type: Animation type ("Idle_Base", "Walk_Base", "Run_Base").
            name: Identifier name for this animation.
            tile_width: Width of each frame in pixels (default: 64).
            tile_height: Height of each frame in pixels (default: 64).

        Returns:
            Dictionary with directions and their animation frames.
        """
        base_path = Path(assets_dir) / "Entities/Characters/Body_A/Animations" / animation_type
        # Find the sprite sheet files (e.g., Run_Down-Sheet.png)
        # Use the first file to determine the base name pattern
        sheet_files = list(base_path.glob("*-Sheet.png"))
        if not sheet_files:
            raise FileNotFoundError(
                f"No sprite sheets found for {animation_type} in {base_path}"
            )

        # Extract base name (e.g., "Run" from "Run_Down-Sheet.png")
        first_file = sheet_files[0].stem  # "Run_Down-Sheet"
        base_name = first_file.rsplit("_", 1)[0]  # "Run"

        return self.load_directional_sprites(
            str(base_path / f"{base_name}"), name, tile_width, tile_height
        )
