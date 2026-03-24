"""
Camera module for PyRPG.

Provides camera functionality for scrolling and following entities.
"""

import pygame
from typing import Optional, Tuple


class Camera:
    """
    2D camera for scrolling and following entities.

    Keeps the player centered while clamping to map bounds.
    """

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        map_width: int,
        map_height: int,
    ):
        """
        Initialize the camera.

        Args:
            screen_width: Width of the screen in pixels.
            screen_height: Height of the screen in pixels.
            map_width: Width of the game map in pixels.
            map_height: Height of the game map in pixels.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height

        # Camera position (top-left corner in world coordinates)
        self.x = 0
        self.y = 0

        # Optional target entity to follow
        self._target: Optional[object] = None

        # Camera smoothing (0.0 = instant, 1.0 = no movement)
        self.smoothing = 0.1

        # Dead zone - area where camera doesn't move (in pixels from center)
        self.dead_zone_x = 0
        self.dead_zone_y = 0

    def set_target(self, target: Optional[object]) -> None:
        """
        Set the entity to follow.

        Args:
            target: Entity with x, y attributes, or None to stop following.
        """
        self._target = target

    def get_target(self) -> Optional[object]:
        """
        Get the current target entity.

        Returns:
            The target entity, or None if not following anything.
        """
        return self._target

    def update(self) -> None:
        """
        Update camera position based on target and settings.
        """
        if self._target is None:
            return

        # Get target center position
        target_center_x = self._target.x + getattr(self._target, 'hitbox_width', 0) // 2
        target_center_y = self._target.y + getattr(self._target, 'hitbox_height', 0) // 2

        # Calculate desired camera position (centered on target)
        desired_x = target_center_x - self.screen_width // 2
        desired_y = target_center_y - self.screen_height // 2

        # Apply dead zone
        if self.dead_zone_x > 0 or self.dead_zone_y > 0:
            # Calculate target position relative to camera center
            target_rel_x = target_center_x - (self.x + self.screen_width // 2)
            target_rel_y = target_center_y - (self.y + self.screen_height // 2)

            # Only update if outside dead zone
            if abs(target_rel_x) > self.dead_zone_x:
                desired_x = self.x + target_rel_x - (self.dead_zone_x if target_rel_x > 0 else -self.dead_zone_x)
            else:
                desired_x = self.x

            if abs(target_rel_y) > self.dead_zone_y:
                desired_y = self.y + target_rel_y - (self.dead_zone_y if target_rel_y > 0 else -self.dead_zone_y)
            else:
                desired_y = self.y

        # Apply smoothing
        if self.smoothing > 0:
            self.x = int(self.x + (desired_x - self.x) * (1 - self.smoothing))
            self.y = int(self.y + (desired_y - self.y) * (1 - self.smoothing))
        else:
            self.x = desired_x
            self.y = desired_y

        # Clamp to map bounds
        self.clamp()

    def clamp(self) -> None:
        """
        Clamp camera position to map bounds.
        """
        # Ensure camera doesn't go beyond map edges
        self.x = max(0, min(self.x, self.map_width - self.screen_width))
        self.y = max(0, min(self.y, self.map_height - self.screen_height))

        # If map is smaller than screen, center the camera
        if self.map_width < self.screen_width:
            self.x = (self.screen_width - self.map_width) // 2
        if self.map_height < self.screen_height:
            self.y = (self.screen_height - self.map_height) // 2

    def set_position(self, x: int, y: int) -> None:
        """
        Set camera position directly.

        Args:
            x: X position in world coordinates.
            y: Y position in world coordinates.
        """
        self.x = x
        self.y = y
        self.clamp()

    def move(self, dx: int, dy: int) -> None:
        """
        Move camera by an offset.

        Args:
            dx: Horizontal offset.
            dy: Vertical offset.
        """
        self.x += dx
        self.y += dy
        self.clamp()

    def get_position(self) -> Tuple[int, int]:
        """
        Get the camera's current position.

        Returns:
            Tuple of (x, y) world coordinates.
        """
        return (self.x, self.y)

    def get_rect(self) -> pygame.Rect:
        """
        Get the camera's visible area in world coordinates.

        Returns:
            pygame.Rect representing the visible area.
        """
        return pygame.Rect(self.x, self.y, self.screen_width, self.screen_height)

    def world_to_screen(self, world_x: int, world_y: int) -> Tuple[int, int]:
        """
        Convert world coordinates to screen coordinates.

        Args:
            world_x: X position in world coordinates.
            world_y: Y position in world coordinates.

        Returns:
            Tuple of (screen_x, screen_y) coordinates.
        """
        screen_x = world_x - self.x
        screen_y = world_y - self.y
        return (screen_x, screen_y)

    def screen_to_world(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """
        Convert screen coordinates to world coordinates.

        Args:
            screen_x: X position on screen.
            screen_y: Y position on screen.

        Returns:
            Tuple of (world_x, world_y) coordinates.
        """
        world_x = screen_x + self.x
        world_y = screen_y + self.y
        return (world_x, world_y)

    def is_visible(self, rect: pygame.Rect) -> bool:
        """
        Check if a rectangle is visible on screen.

        Args:
            rect: Rectangle in world coordinates.

        Returns:
            True if the rectangle is at least partially visible.
        """
        camera_rect = self.get_rect()
        return camera_rect.colliderect(rect)

    def set_smoothing(self, smoothing: float) -> None:
        """
        Set camera smoothing factor.

        Args:
            smoothing: Value between 0.0 (instant) and 1.0 (no movement).
        """
        self.smoothing = max(0.0, min(1.0, smoothing))

    def set_dead_zone(self, width: int, height: int) -> None:
        """
        Set the camera dead zone.

        Args:
            width: Horizontal dead zone size in pixels.
            height: Vertical dead zone size in pixels.
        """
        self.dead_zone_x = max(0, width)
        self.dead_zone_y = max(0, height)
