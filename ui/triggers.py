"""
Triggers module for PyRPG.

Provides trigger zone functionality similar to Unity's OnTriggerEnter2D.
"""

import pygame
from typing import Callable, Optional, Any, List


class TriggerZone:
    """
    A rectangular trigger zone that detects when entities enter or exit.

    Similar to Unity's Trigger2D collider system.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        trigger_id: Optional[str] = None,
        one_shot: bool = False,
    ):
        """
        Initialize a trigger zone.

        Args:
            x: X position in world pixels.
            y: Y position in world pixels.
            width: Width of the trigger zone in pixels.
            height: Height of the trigger zone in pixels.
            trigger_id: Unique identifier for this trigger (auto-generated if None).
            one_shot: If True, trigger only fires once then becomes inactive.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.trigger_id = trigger_id or f"trigger_{x}_{y}"
        self.one_shot = one_shot
        self._has_triggered = False
        self._is_active = True

        # Callbacks - similar to Unity's event system
        self.on_enter: Optional[Callable[[Any], None]] = None
        self.on_exit: Optional[Callable[[Any], None]] = None
        self.on_stay: Optional[Callable[[Any], None]] = None

        # Track which entities are currently in the trigger
        self._entities_inside: set = set()

    def check_trigger(self, entity_rect: pygame.Rect, entity_id: Any = None) -> None:
        """
        Check if an entity is triggering this zone and call appropriate callbacks.

        Args:
            entity_rect: The entity's collision rectangle.
            entity_id: Optional identifier for the entity (defaults to rect id).
        """
        if not self._is_active:
            return

        if entity_id is None:
            entity_id = id(entity_rect)

        is_colliding = self.rect.colliderect(entity_rect)

        if is_colliding:
            # Entity entered or staying
            if entity_id not in self._entities_inside:
                # Just entered - fire on_enter
                self._entities_inside.add(entity_id)
                if self.on_enter:
                    self.on_enter(entity_id)

                # Handle one-shot triggers
                if self.one_shot and not self._has_triggered:
                    self._has_triggered = True
                    self._is_active = False
            else:
                # Already inside - fire on_stay
                if self.on_stay:
                    self.on_stay(entity_id)
        else:
            # Entity exited
            if entity_id in self._entities_inside:
                self._entities_inside.remove(entity_id)
                if self.on_exit:
                    self.on_exit(entity_id)

    def reset(self) -> None:
        """Reset the trigger zone (clears one-shot state and tracked entities)."""
        self._has_triggered = False
        self._is_active = True
        self._entities_inside.clear()

    def deactivate(self) -> None:
        """Deactivate the trigger zone (no longer detects collisions)."""
        self._is_active = False

    def activate(self) -> None:
        """Activate the trigger zone."""
        self._is_active = True

    def has_triggered(self) -> bool:
        """Check if this one-shot trigger has already fired."""
        return self._has_triggered

    def is_active(self) -> bool:
        """Check if the trigger is currently active."""
        return self._is_active

    def contains_point(self, x: int, y: int) -> bool:
        """
        Check if a point is inside the trigger zone.

        Args:
            x: X coordinate in world pixels.
            y: Y coordinate in world pixels.

        Returns:
            True if the point is inside the trigger zone.
        """
        return self.rect.collidepoint(x, y)

    def set_position(self, x: int, y: int) -> None:
        """
        Set the trigger zone's position.

        Args:
            x: New X position.
            y: New Y position.
        """
        self.rect.x = x
        self.rect.y = y

    def get_position(self) -> tuple[int, int]:
        """
        Get the trigger zone's position.

        Returns:
            Tuple of (x, y) coordinates.
        """
        return (self.rect.x, self.rect.y)

    def get_rect(self) -> pygame.Rect:
        """
        Get the trigger zone's rectangle.

        Returns:
            pygame.Rect representing the trigger zone.
        """
        return self.rect.copy()

    def draw(
        self,
        screen: pygame.Surface,
        color: tuple[int, int, int] = (255, 0, 0, 128),
        width: int = 2,
        camera_x: int = 0,
        camera_y: int = 0,
    ) -> None:
        """
        Draw the trigger zone for debugging.

        Args:
            screen: Pygame surface to draw on.
            color: Color of the trigger outline (R, G, B).
            width: Width of the outline in pixels.
            camera_x: X offset for camera scrolling.
            camera_y: Y offset for camera scrolling.
        """
        # Create a temporary surface for alpha blending
        debug_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        alpha_color = (*color[:3], 128)  # Add alpha channel
        pygame.draw.rect(debug_surface, alpha_color, debug_surface.get_rect(), width)

        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y
        screen.blit(debug_surface, (screen_x, screen_y))


class TriggerManager:
    """
    Manages multiple trigger zones and updates them efficiently.
    """

    def __init__(self):
        """Initialize the TriggerManager."""
        self.triggers: List[TriggerZone] = []
        self._trigger_map: dict[str, TriggerZone] = {}

    def add_trigger(self, trigger: TriggerZone) -> None:
        """
        Add a trigger zone to the manager.

        Args:
            trigger: The TriggerZone to add.
        """
        self.triggers.append(trigger)
        self._trigger_map[trigger.trigger_id] = trigger

    def remove_trigger(self, trigger_id: str) -> Optional[TriggerZone]:
        """
        Remove a trigger zone by ID.

        Args:
            trigger_id: ID of the trigger to remove.

        Returns:
            The removed TriggerZone, or None if not found.
        """
        if trigger_id in self._trigger_map:
            trigger = self._trigger_map.pop(trigger_id)
            self.triggers.remove(trigger)
            return trigger
        return None

    def get_trigger(self, trigger_id: str) -> Optional[TriggerZone]:
        """
        Get a trigger zone by ID.

        Args:
            trigger_id: ID of the trigger to get.

        Returns:
            The TriggerZone, or None if not found.
        """
        return self._trigger_map.get(trigger_id)

    def update_all(self, entity_rect: pygame.Rect, entity_id: Any = None) -> None:
        """
        Update all triggers with an entity's position.

        Args:
            entity_rect: The entity's collision rectangle.
            entity_id: Optional identifier for the entity.
        """
        for trigger in self.triggers:
            trigger.check_trigger(entity_rect, entity_id)

    def draw_all(
        self,
        screen: pygame.Surface,
        color: tuple[int, int, int] = (255, 0, 0, 128),
        width: int = 2,
        camera_x: int = 0,
        camera_y: int = 0,
    ) -> None:
        """
        Draw all trigger zones for debugging.

        Args:
            screen: Pygame surface to draw on.
            color: Color of the trigger outlines.
            width: Width of the outlines.
            camera_x: X offset for camera scrolling.
            camera_y: Y offset for camera scrolling.
        """
        for trigger in self.triggers:
            trigger.draw(screen, color, width, camera_x, camera_y)

    def clear(self) -> None:
        """Remove all triggers."""
        self.triggers.clear()
        self._trigger_map.clear()
