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
        idle_animations: Dict[str, List[pygame.Surface]],
        walk_animations: Optional[Dict[str, List[pygame.Surface]]] = None,
        run_animations: Optional[Dict[str, List[pygame.Surface]]] = None,
        walk_speed: int = 2,
        run_speed: int = 4,
        animation_speed: float = 0.15,
        scale: int = 3,
        hitbox_width: int = 24,
        hitbox_height: int = 40,
        hitbox_offset_x: int = 0,
        hitbox_offset_y: int = 0,
    ):
        """
        Initialize the player.

        Args:
            x: Initial X position.
            y: Initial Y position.
            idle_animations: Dictionary with direction keys and idle frame lists.
            walk_animations: Dictionary with direction keys and walk frame lists.
            run_animations: Dictionary with direction keys and run frame lists.
            walk_speed: Walking speed in pixels per frame.
            run_speed: Running speed in pixels per frame.
            animation_speed: Animation speed (lower = slower).
            scale: Scale factor for sprite rendering (default: 3).
            hitbox_width: Width of collision box in pixels.
            hitbox_height: Height of collision box in pixels.
            hitbox_offset_x: Horizontal offset from sprite position.
            hitbox_offset_y: Vertical offset from sprite position.
        """
        self.x = x
        self.y = y
        self.idle_animations = idle_animations
        self.walk_animations = walk_animations or idle_animations
        self.run_animations = run_animations or walk_animations or idle_animations

        self.walk_speed = walk_speed
        self.run_speed = run_speed
        self.speed = walk_speed
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
        self._is_running = False
        self._idle_frames = self._get_idle_frames()
        self._scaled_cache: Dict[str, pygame.Surface] = {}

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
        if not self._is_moving:
            return self.idle_animations
        elif self._is_running:
            return self.run_animations
        else:
            return self.walk_animations

    def set_running(self, running: bool) -> None:
        """
        Set running state.

        Args:
            running: True to run, False to walk.
        """
        self._is_running = running
        self.speed = self.run_speed if running else self.walk_speed

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

    def try_move(self, dx: int, dy: int, blocked_x: bool, blocked_y: bool) -> None:
        """
        Attempt to move the player with collision blocking.

        Args:
            dx: Intended horizontal movement (-1, 0, 1).
            dy: Intended vertical movement (-1, 0, 1).
            blocked_x: If True, horizontal movement is blocked.
            blocked_y: If True, vertical movement is blocked.
        """
        if dx != 0 or dy != 0:
            # Update direction based on intended movement
            if dx > 0:
                self.direction = "right"
            elif dx < 0:
                self.direction = "left"
            elif dy > 0:
                self.direction = "down"
            elif dy < 0:
                self.direction = "up"

            # Apply movement only if not blocked
            moved = False
            if not blocked_x:
                self.x += dx * self.speed
                moved = True
            if not blocked_y:
                self.y += dy * self.speed
                moved = True

            # Update animation only if actually moved
            if moved:
                self._is_moving = True
                self._update_animation()
            else:
                self._is_moving = False
                self.animation_counter = 0.0
                self.frame_index = 0
        else:
            self._is_moving = False
            self.animation_counter = 0.0
            self.frame_index = 0

    def _update_animation(self) -> None:
        """Update the current animation frame."""
        self.animation_counter += self.animation_speed
        animations = self._get_current_animations()
        frames = animations[self.direction]
        max_frames = len(frames)

        if self.animation_counter >= max_frames:
            self.animation_counter = 0.0

        self.frame_index = int(self.animation_counter)

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
            pygame.Rect representing player's bounding box (scaled).
        """
        return pygame.Rect(
            self.x + self.hitbox_offset_x,
            self.y + self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height,
        )

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
