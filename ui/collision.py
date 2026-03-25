"""
Collision detection module for PyRPG.

Provides utilities for detecting and resolving collisions between game entities.
"""

import pygame
from typing import List, Optional, Tuple


def check_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """
    Check if two rectangles collide.

    Args:
        rect1: First rectangle.
        rect2: Second rectangle.

    Returns:
        True if the rectangles overlap, False otherwise.
    """
    return rect1.colliderect(rect2)


def check_multiple_collisions(
    player_rect: pygame.Rect, npc_rects: List[pygame.Rect]
) -> List[int]:
    """
    Check if player collides with any of multiple NPCs.

    Args:
        player_rect: Player's collision rectangle.
        npc_rects: List of NPC collision rectangles.

    Returns:
        List of indices of NPCs that are colliding with the player.
    """
    colliding_indices = []
    for i, npc_rect in enumerate(npc_rects):
        if check_collision(player_rect, npc_rect):
            colliding_indices.append(i)
    return colliding_indices


def resolve_collision(
    player: object,
    npc: object,
    dx: int,
    dy: int,
) -> Tuple[bool, bool]:
    """
    Resolve collision between player and NPC by blocking movement.

    This function checks if the player's intended movement would cause
    a collision with the NPC, and returns adjusted movement values.

    Args:
        player: Player object with get_rect() and x, y attributes.
        npc: NPC object with get_rect() method.
        dx: Intended horizontal movement (-1, 0, 1).
        dy: Intended vertical movement (-1, 0, 1).

    Returns:
        Tuple of (blocked_x, blocked_y) where True means movement is blocked.
    """
    player_rect = player.get_rect()

    # Calculate potential new position
    new_x = player.x + dx * player.speed
    new_y = player.y + dy * player.speed

    # Create test rectangles for each axis, preserving hitbox offsets
    test_rect_x = pygame.Rect(
        new_x + player.hitbox_offset_x,
        player.y + player.hitbox_offset_y,
        player_rect.width,
        player_rect.height,
    )
    test_rect_y = pygame.Rect(
        player.x + player.hitbox_offset_x,
        new_y + player.hitbox_offset_y,
        player_rect.width,
        player_rect.height,
    )

    npc_rect = npc.get_rect()

    blocked_x = test_rect_x.colliderect(npc_rect)
    blocked_y = test_rect_y.colliderect(npc_rect)

    return blocked_x, blocked_y


def resolve_multiple_collisions(
    player: object,
    npcs: List[object],
    dx: int,
    dy: int,
) -> Tuple[bool, bool]:
    """
    Resolve collisions between player and multiple NPCs.

    Args:
        player: Player object with get_rect() and x, y attributes.
        npcs: List of NPC objects with get_rect() method.
        dx: Intended horizontal movement (-1, 0, 1).
        dy: Intended vertical movement (-1, 0, 1).

    Returns:
        Tuple of (blocked_x, blocked_y) where True means movement is blocked.
    """
    player_rect = player.get_rect()

    # Calculate potential new position
    new_x = player.x + dx * player.speed
    new_y = player.y + dy * player.speed

    # Create test rectangles for each axis, preserving hitbox offsets
    test_rect_x = pygame.Rect(
        new_x + player.hitbox_offset_x,
        player.y + player.hitbox_offset_y,
        player_rect.width,
        player_rect.height,
    )
    test_rect_y = pygame.Rect(
        player.x + player.hitbox_offset_x,
        new_y + player.hitbox_offset_y,
        player_rect.width,
        player_rect.height,
    )

    blocked_x = False
    blocked_y = False

    for npc in npcs:
        npc_rect = npc.get_rect()
        if not blocked_x and test_rect_x.colliderect(npc_rect):
            blocked_x = True
        if not blocked_y and test_rect_y.colliderect(npc_rect):
            blocked_y = True

        # Early exit if both directions are blocked
        if blocked_x and blocked_y:
            break

    return blocked_x, blocked_y


def get_collision_direction(player_rect: pygame.Rect, npc_rect: pygame.Rect) -> Optional[str]:
    """
    Determine the relative direction of collision between player and NPC.

    Args:
        player_rect: Player's collision rectangle.
        npc_rect: NPC's collision rectangle.

    Returns:
        String indicating which side of the NPC the player is colliding with
        ("top", "bottom", "left", "right"), or None if not colliding.
    """
    if not player_rect.colliderect(npc_rect):
        return None

    # Calculate overlap in each direction
    player_center_x = player_rect.centerx
    player_center_y = player_rect.centery
    npc_center_x = npc_rect.centerx
    npc_center_y = npc_rect.centery

    dx = player_center_x - npc_center_x
    dy = player_center_y - npc_center_y

    # Determine which axis has less overlap (collision side)
    if abs(dx) > abs(dy):
        return "right" if dx > 0 else "left"
    else:
        return "bottom" if dy > 0 else "top"
