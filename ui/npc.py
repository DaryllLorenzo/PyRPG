"""
NPC module for PyRPG.

Contains the NPC class with sprite animations for non-player characters.
"""

import pygame
from typing import Dict, List, Optional


class NPC:
    """Non-player character with animated sprites."""

    def __init__(
        self,
        x: int,
        y: int,
        idle_animations: Dict[str, List[pygame.Surface]],
        walk_animations: Optional[Dict[str, List[pygame.Surface]]] = None,
        animation_speed: float = 0.15,
        scale: int = 3,
        hitbox_width: int = 24,
        hitbox_height: int = 40,
        hitbox_offset_x: int = 0,
        hitbox_offset_y: int = 0,
    ):
        """
        Initialize the NPC.

        Args:
            x: Initial X position.
            y: Initial Y position.
            idle_animations: Dictionary with direction keys and idle frame lists.
            walk_animations: Dictionary with direction keys and walk frame lists.
            animation_speed: Animation speed (lower = slower).
            scale: Scale factor for sprite rendering.
            hitbox_width: Width of collision box in pixels.
            hitbox_height: Height of collision box in pixels.
            hitbox_offset_x: Horizontal offset from sprite position.
            hitbox_offset_y: Vertical offset from sprite position.
        """
        self.x = x
        self.y = y
        self.idle_animations = idle_animations
        self.walk_animations = walk_animations or idle_animations

        self.animation_speed = animation_speed
        self.scale = scale
        self.hitbox_width = hitbox_width
        self.hitbox_height = hitbox_height
        self.hitbox_offset_x = hitbox_offset_x
        self.hitbox_offset_y = hitbox_offset_y

        self.direction = "down"
        self.frame_index = 0
        self.animation_counter = 0.0

        self._is_moving = False
        self._idle_frames = self._get_idle_frames()

    def _get_idle_frames(self) -> Dict[str, pygame.Surface]:
        """Get the first frame of each direction for idle state."""
        return {
            "up": self.idle_animations["up"][0],
            "right": self.idle_animations["right"][0],
            "down": self.idle_animations["down"][0],
            "left": self.idle_animations["left"][0],
        }

    def _get_current_animations(self) -> Dict[str, List[pygame.Surface]]:
        """Get the current animation set based on movement state."""
        if self._is_moving:
            return self.walk_animations
        else:
            return self.idle_animations

    def set_direction(self, direction: str) -> None:
        """
        Set the NPC's facing direction.

        Args:
            direction: One of "up", "down", "left", "right".
        """
        if direction in ("up", "down", "left", "right"):
            self.direction = direction

    def update_animation(self) -> None:
        """Update the current animation frame."""
        if self._is_moving:
            self.animation_counter += self.animation_speed
            animations = self._get_current_animations()
            frames = animations[self.direction]
            max_frames = len(frames)

            if self.animation_counter >= max_frames:
                self.animation_counter = 0.0

            self.frame_index = int(self.animation_counter)
        else:
            self.animation_counter = 0.0
            self.frame_index = 0

    def get_current_frame(self) -> pygame.Surface:
        """
        Get the current sprite frame (scaled).

        Returns:
            The current pygame.Surface for rendering (scaled).
        """
        if self._is_moving:
            animations = self._get_current_animations()
            frame = animations[self.direction][self.frame_index]
        else:
            frame = self._idle_frames[self.direction]

        # Scale the frame
        scaled_size = (frame.get_width() * self.scale, frame.get_height() * self.scale)
        return pygame.transform.scale(frame, scaled_size)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the NPC on the screen.

        Args:
            screen: Pygame surface to draw on.
        """
        frame = self.get_current_frame()
        screen.blit(frame, (self.x, self.y))

    def get_rect(self) -> pygame.Rect:
        """
        Get the collision rectangle for the NPC.

        Returns:
            pygame.Rect representing NPC's bounding box (scaled).
        """
        return pygame.Rect(
            self.x + self.hitbox_offset_x,
            self.y + self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height,
        )

    def set_position(self, x: int, y: int) -> None:
        """
        Set the NPC's position directly.

        Args:
            x: New X position.
            y: New Y position.
        """
        self.x = x
        self.y = y

    def get_position(self) -> tuple[int, int]:
        """
        Get the current position.

        Returns:
            Tuple of (x, y) coordinates.
        """
        return (self.x, self.y)
