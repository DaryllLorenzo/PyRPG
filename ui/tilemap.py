"""
TileMap module for PyRPG.

Handles loading and rendering tile-based floor maps.
"""

import pygame
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TileMap:
    """Manages tile-based floor rendering."""

    def __init__(
        self,
        tile_size: int = 16,
        map_width: int = 40,
        map_height: int = 30,
    ):
        """
        Initialize the TileMap.

        Args:
            tile_size: Size of each tile in pixels (default: 16).
            map_width: Width of the map in tiles.
            map_height: Height of the map in tiles.
        """
        self.tile_size = tile_size
        self.map_width = map_width
        self.map_height = map_height
        self.pixel_width = map_width * tile_size
        self.pixel_height = map_height * tile_size

        # 2D array storing tile indices: tilemap[y][x] = tile_id
        self.tilemap: List[List[int]] = [[0 for _ in range(map_width)] for _ in range(map_height)]

        # Loaded tile images: tile_id -> pygame.Surface
        self.tiles: Dict[int, pygame.Surface] = {}

        # Default fill tile (usually 0 = grass or basic floor)
        self.default_tile = 0

    def load_tileset(
        self,
        tileset_path: str,
        tile_id_start: int = 0,
        columns: Optional[int] = None,
        rows: Optional[int] = None,
    ) -> int:
        """
        Load a tileset image and extract individual tiles.

        The sprite sheet should have a grid of tiles.

        Args:
            tileset_path: Path to the tileset image.
            tile_id_start: Starting ID for these tiles (default: 0).
            columns: Number of columns in tileset (auto-detected if None).
            rows: Number of rows in tileset (auto-detected if None).

        Returns:
            Number of tiles loaded.
        """
        path = Path(tileset_path)
        if not path.exists():
            raise FileNotFoundError(f"Tileset not found: {tileset_path}")

        # Load image and convert to surface with alpha channel
        tileset_image = pygame.image.load(str(path))
        # Create a new surface with per-pixel alpha for transparency support
        if tileset_image.get_alpha() is None:
            converted = pygame.Surface(tileset_image.get_size(), pygame.SRCALPHA)
            converted.blit(tileset_image, (0, 0))
            tileset_image = converted

        # Auto-detect dimensions
        if columns is None:
            columns = tileset_image.get_width() // self.tile_size
        if rows is None:
            rows = tileset_image.get_height() // self.tile_size

        # Extract each tile
        tile_id = tile_id_start
        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(
                    col * self.tile_size,
                    row * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )

                # Only extract if within image bounds
                if rect.right <= tileset_image.get_width() and rect.bottom <= tileset_image.get_height():
                    try:
                        tile_surface = tileset_image.subsurface(rect).copy()
                        self.tiles[tile_id] = tile_surface
                    except pygame.error:
                        # Skip tiles that can't be extracted
                        pass
                    tile_id += 1

        return tile_id - tile_id_start

    def set_tile(self, x: int, y: int, tile_id: int) -> None:
        """
        Set a tile at a specific position.

        Args:
            x: X position in tiles (grid coordinates).
            y: Y position in tiles (grid coordinates).
            tile_id: ID of the tile to place.
        """
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            self.tilemap[y][x] = tile_id

    def get_tile(self, x: int, y: int) -> int:
        """
        Get the tile ID at a specific position.

        Args:
            x: X position in tiles (grid coordinates).
            y: Y position in tiles (grid coordinates).

        Returns:
            Tile ID at the position.
        """
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            return self.tilemap[y][x]
        return -1  # Out of bounds

    def fill_rect(
        self,
        start_x: int,
        start_y: int,
        width: int,
        height: int,
        tile_id: int,
    ) -> None:
        """
        Fill a rectangular area with a specific tile.

        Args:
            start_x: Starting X position in tiles.
            start_y: Starting Y position in tiles.
            width: Width in tiles.
            height: Height in tiles.
            tile_id: Tile ID to fill with.
        """
        for y in range(start_y, min(start_y + height, self.map_height)):
            for x in range(start_x, min(start_x + width, self.map_width)):
                self.tilemap[y][x] = tile_id

    def fill_all(self, tile_id: int) -> None:
        """
        Fill the entire map with a specific tile.

        Args:
            tile_id: Tile ID to fill with.
        """
        self.fill_rect(0, 0, self.map_width, self.map_height, tile_id)

    def draw(
        self,
        screen: pygame.Surface,
        camera_x: int = 0,
        camera_y: int = 0,
    ) -> None:
        """
        Draw the tilemap on the screen.

        Args:
            screen: Pygame surface to draw on.
            camera_x: X offset for camera scrolling.
            camera_y: Y offset for camera scrolling.
        """
        # Calculate visible tile range based on camera
        start_tile_x = max(0, camera_x // self.tile_size)
        start_tile_y = max(0, camera_y // self.tile_size)
        end_tile_x = min(self.map_width, (camera_x + screen.get_width()) // self.tile_size + 1)
        end_tile_y = min(self.map_height, (camera_y + screen.get_height()) // self.tile_size + 1)

        # Draw visible tiles
        for y in range(start_tile_y, end_tile_y):
            for x in range(start_tile_x, end_tile_x):
                tile_id = self.tilemap[y][x]
                if tile_id in self.tiles:
                    tile_surface = self.tiles[tile_id]
                    screen_x = x * self.tile_size - camera_x
                    screen_y = y * self.tile_size - camera_y
                    screen.blit(tile_surface, (screen_x, screen_y))

    def world_to_tile(self, world_x: int, world_y: int) -> Tuple[int, int]:
        """
        Convert world pixel coordinates to tile grid coordinates.

        Args:
            world_x: X position in world pixels.
            world_y: Y position in world pixels.

        Returns:
            Tuple of (tile_x, tile_y) grid coordinates.
        """
        tile_x = world_x // self.tile_size
        tile_y = world_y // self.tile_size
        return (tile_x, tile_y)

    def tile_to_world(self, tile_x: int, tile_y: int) -> Tuple[int, int]:
        """
        Convert tile grid coordinates to world pixel coordinates.

        Args:
            tile_x: X position in tiles.
            tile_y: Y position in tiles.

        Returns:
            Tuple of (world_x, world_y) pixel coordinates (top-left of tile).
        """
        world_x = tile_x * self.tile_size
        world_y = tile_y * self.tile_size
        return (world_x, world_y)

    def get_tile_rect(self, tile_x: int, tile_y: int) -> pygame.Rect:
        """
        Get the world-space rectangle for a tile.

        Args:
            tile_x: X position in tiles.
            tile_y: Y position in tiles.

        Returns:
            pygame.Rect representing the tile's world-space bounds.
        """
        x, y = self.tile_to_world(tile_x, tile_y)
        return pygame.Rect(x, y, self.tile_size, self.tile_size)

    def get_bounds(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the entire map.

        Returns:
            pygame.Rect representing the map bounds.
        """
        return pygame.Rect(0, 0, self.pixel_width, self.pixel_height)

    def generate_basic_tile(
        self,
        tile_type: str = "grass",
        variation: int = 0,
    ) -> pygame.Surface:
        """
        Generate a basic tile programmatically.

        Creates a simple, repeatable tile pattern without visual conflicts.

        Args:
            tile_type: Type of tile ("grass", "dirt", "stone", "sand").
            variation: Variation index (0-3) for visual variety.

        Returns:
            pygame.Surface of the generated tile.
        """
        tile = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)

        if tile_type == "grass":
            # Base grass color with variation
            base_green = 34 + (variation * 3)
            grass_color = (base_green, 139 + variation, base_green - 10)
            tile.fill(grass_color)

            # Add subtle grass blade details
            for i in range(4 + variation):
                x = (i * 4 + variation * 2) % self.tile_size
                y = (i * 3) % self.tile_size
                blade_color = (base_green + 5, 149 + variation, base_green - 5)
                pygame.draw.line(tile, blade_color, (x, y), (x, y + 3), 1)

        elif tile_type == "dirt":
            # Base dirt color
            dirt_base = 101 + (variation * 5)
            dirt_color = (dirt_base, 67, 33)
            tile.fill(dirt_color)

            # Add small pebbles
            pebble_positions = [
                (3 + variation, 4),
                (8, 10 + variation),
                (12 - variation, 6),
                (6, 13),
            ]
            for px, py in pebble_positions:
                if 0 <= px < self.tile_size and 0 <= py < self.tile_size:
                    pebble_color = (dirt_base - 10, 57, 23)
                    pygame.draw.circle(tile, pebble_color, (px, py), 2)

        elif tile_type == "stone":
            # Base stone color
            stone_gray = 100 + (variation * 8)
            stone_color = (stone_gray, stone_gray, stone_gray + 10)
            tile.fill(stone_color)

            # Add stone texture lines
            for i in range(3):
                y = 4 + i * 4 + variation
                if y < self.tile_size:
                    line_color = (stone_gray - 20, stone_gray - 20, stone_gray - 15)
                    pygame.draw.line(tile, line_color, (0, y), (self.tile_size, y), 1)

        elif tile_type == "sand":
            # Base sand color
            sand_yellow = 210 + (variation * 3)
            sand_color = (sand_yellow, 180 + variation, 100)
            tile.fill(sand_color)

            # Add sand grain details
            for i in range(5 + variation):
                x = (i * 3 + variation) % self.tile_size
                y = (i * 2) % self.tile_size
                grain_color = (sand_yellow - 20, 170 + variation, 90)
                pygame.draw.circle(tile, grain_color, (x, y), 1)

        else:
            # Default to grass
            tile.fill((34, 139, 34))

        return tile
