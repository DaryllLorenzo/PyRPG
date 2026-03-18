"""
Player module for PyRPG.

Contains the Player class with sprite animations and movement.
"""

import pygame
from typing import Dict, List, Optional


class Player:
    """Player character with animated sprites and movement."""

    def __init__(
        self,
        x: int,
        y: int,
        animations: Dict[str, List[pygame.Surface]],
        speed: int = 2,
        animation_speed: float = 0.15,
    ):
        """
        Initialize the player.

        Args:
            x: Initial X position.
            y: Initial Y position.
            animations: Dictionary with direction keys and frame lists.
            speed: Movement speed in pixels per frame.
            animation_speed: Animation speed (lower = slower).
        """
        self.x = x
        self.y = y
        self.animations = animations
        self.speed = speed
        self.animation_speed = animation_speed

        self.direction = "down"
        self.frame_index = 0
        self.animation_counter = 0.0

        self._is_moving = False
        self._idle_frames = self._get_idle_frames()

    def _get_idle_frames(self) -> Dict[str, pygame.Surface]:
        """Get the first frame of each direction for idle state."""
        return {
            "up": self.animations["up"][0],
            "right": self.animations["right"][0],
            "down": self.animations["down"][0],
            "left": self.animations["left"][0],
        }

    def move(self, dx: int, dy: int) -> None:
        """
        Move the player and update animation.

        Args:
            dx: Horizontal movement (-1, 0, 1).
            dy: Vertical movement (-1, 0, 1).
        """
        if dx != 0 or dy != 0:
            self._is_moving = True

            # Update direction based on movement
            if dx > 0:
                self.direction = "right"
            elif dx < 0:
                self.direction = "left"
            elif dy > 0:
                self.direction = "down"
            elif dy < 0:
                self.direction = "up"

            # Move player
            self.x += dx * self.speed
            self.y += dy * self.speed

            # Update animation
            self._update_animation()
        else:
            self._is_moving = False
            self.animation_counter = 0.0
            self.frame_index = 0

    def _update_animation(self) -> None:
        """Update the current animation frame."""
        self.animation_counter += self.animation_speed
        frames = self.animations[self.direction]
        max_frames = len(frames)

        if self.animation_counter >= max_frames:
            self.animation_counter = 0.0

        self.frame_index = int(self.animation_counter)

    def get_current_frame(self) -> pygame.Surface:
        """
        Get the current sprite frame.

        Returns:
            The current pygame.Surface for rendering.
        """
        if self._is_moving:
            return self.animations[self.direction][self.frame_index]
        else:
            return self._idle_frames[self.direction]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the player on the screen.

        Args:
            screen: Pygame surface to draw on.
        """
        frame = self.get_current_frame()
        screen.blit(frame, (self.x, self.y))

    def get_rect(self) -> pygame.Rect:
        """
        Get the collision rectangle for the player.

        Returns:
            pygame.Rect representing player's bounding box.
        """
        frame = self.get_current_frame()
        return pygame.Rect(self.x, self.y, frame.get_width(), frame.get_height())

    def set_position(self, x: int, y: int) -> None:
        """
        Set the player's position directly.

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
