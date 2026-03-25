"""
Dialog Box module for PyRPG.

Provides a dialog box UI component for NPC conversations.
"""

import pygame
from typing import Optional, List
from pathlib import Path


class DialogBox:
    """
    Dialog box UI component with smooth animations.

    Displays a banner at the bottom of the screen with:
    - NPC portrait on the left
    - White text area with blue decorative borders
    """

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        portrait_path: Optional[str] = None,
        portrait_scale: int = 3,
        animation_speed: float = 0.15,
    ):
        """
        Initialize the dialog box.

        Args:
            screen_width: Width of the game screen.
            screen_height: Height of the game screen.
            portrait_path: Path to the NPC portrait image.
            portrait_scale: Scale factor for the portrait.
            animation_speed: Speed of the open/close animation (0.0-1.0).
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Dialog box dimensions - adjusted for 800x600 screen
        self.box_height = 130
        self.border_height = 6
        self.portrait_margin = 12
        self.text_margin = 8

        # Calculate portrait dimensions
        self.portrait_scale = portrait_scale
        self._original_portrait: Optional[pygame.Surface] = None
        self.portrait: Optional[pygame.Surface] = None
        self.portrait_width = 0
        self.portrait_height = 0

        # Load portrait if path provided
        if portrait_path:
            self.load_portrait(portrait_path)

        # Animation state
        self._is_open = False
        self._is_animating = False
        self._current_y = screen_height  # Start hidden (below screen)
        self._target_y = screen_height - self.box_height  # Final position
        self.animation_speed = animation_speed

        # Text state
        self._full_text = ""
        self._displayed_text = ""
        self._char_index = 0
        self._char_timer = 0
        self._char_delay = 30  # ms between characters

        # Colors
        self.color_white = (255, 255, 255)
        self.color_blue_dark = (40, 80, 160)
        self.color_blue_light = (60, 120, 200)
        self.color_black = (0, 0, 0)
        self.color_border = (30, 30, 50)

        # Font
        self.font = pygame.font.Font(None, 26)

    def load_portrait(self, path: str) -> None:
        """
        Load and scale the NPC portrait.

        Args:
            path: Path to the portrait image.
        """
        portrait_file = Path(path)
        if not portrait_file.exists():
            print(f"Portrait not found: {path}")
            return

        self._original_portrait = pygame.image.load(str(portrait_file)).convert_alpha()

        # Calculate max portrait size based on dialog box dimensions
        # Portrait should fit in the content area with margins
        max_portrait_height = self.box_height - (self.border_height * 2) - 16
        max_portrait_width = 80  # Fixed width for portrait area

        # Scale the portrait to fit within max dimensions
        original_width = self._original_portrait.get_width()
        original_height = self._original_portrait.get_height()

        # Calculate scale factor to fit
        scale_x = max_portrait_width / original_width
        scale_y = max_portrait_height / original_height
        scale = min(scale_x, scale_y)

        self.portrait_width = int(original_width * scale)
        self.portrait_height = int(original_height * scale)

        self.portrait = pygame.transform.scale(
            self._original_portrait,
            (self.portrait_width, self.portrait_height),
        )

    def set_text(self, text: str) -> None:
        """
        Set the dialog text to display.

        Args:
            text: The full text to display (will be typed out).
        """
        self._full_text = text
        self._displayed_text = ""
        self._char_index = 0
        self._char_timer = 0

    def open(self) -> None:
        """Start the open animation."""
        self._is_open = True
        self._is_animating = True

    def close(self) -> None:
        """Start the close animation."""
        self._is_open = False
        self._is_animating = True

    def is_open(self) -> bool:
        """Check if the dialog box is fully open."""
        return self._is_open and not self._is_animating

    def is_closed(self) -> bool:
        """Check if the dialog box is fully closed."""
        return not self._is_open and not self._is_animating

    def is_text_complete(self) -> bool:
        """Check if all text has been displayed."""
        return self._char_index >= len(self._full_text)

    def update(self, dt: int) -> None:
        """
        Update the dialog box state.

        Args:
            dt: Delta time in milliseconds.
        """
        # Update animation
        if self._is_animating:
            if self._is_open:
                # Animate opening (slide up)
                self._current_y += (self._target_y - self._current_y) * self.animation_speed
                if abs(self._current_y - self._target_y) < 1:
                    self._current_y = self._target_y
                    self._is_animating = False
            else:
                # Animate closing (slide down)
                target_y = self.screen_height
                self._current_y += (target_y - self._current_y) * self.animation_speed
                if abs(self._current_y - target_y) < 1:
                    self._current_y = target_y
                    self._is_animating = False

        # Update text typing
        if self._is_open and not self._is_animating:
            if self._char_index < len(self._full_text):
                self._char_timer += dt
                if self._char_timer >= self._char_delay:
                    self._displayed_text += self._full_text[self._char_index]
                    self._char_index += 1
                    self._char_timer = 0

    def advance_text(self) -> bool:
        """
        Advance the text display.

        Returns:
            True if there's more text to show, False if text is complete.
        """
        if self._char_index < len(self._full_text):
            # Show all remaining text
            self._displayed_text = self._full_text
            self._char_index = len(self._full_text)
            return False
        return True

    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """
        Wrap text to fit within the given width.

        Args:
            text: Text to wrap.
            max_width: Maximum width in pixels.

        Returns:
            List of wrapped lines.
        """
        words = text.split(" ")
        lines: List[str] = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_width = self.font.size(test_line)[0]

            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the dialog box on the screen.

        Args:
            screen: Pygame surface to draw on.
        """
        if self._is_animating and not self._is_open and self._current_y >= self.screen_height - 1:
            return  # Don't draw when fully closed and animating out

        # Calculate layout
        box_rect = pygame.Rect(
            0,
            int(self._current_y),
            self.screen_width,
            self.box_height,
        )

        # Draw top blue border
        top_border_rect = pygame.Rect(
            0,
            int(self._current_y),
            self.screen_width,
            self.border_height,
        )
        pygame.draw.rect(screen, self.color_blue_dark, top_border_rect)

        # Draw main content area
        content_y = int(self._current_y) + self.border_height
        content_height = self.box_height - (self.border_height * 2)

        # Background
        content_rect = pygame.Rect(
            0,
            content_y,
            self.screen_width,
            content_height,
        )
        pygame.draw.rect(screen, self.color_white, content_rect)

        # Draw portrait (if loaded)
        if self.portrait:
            portrait_x = self.portrait_margin
            portrait_y = content_y + (content_height - self.portrait_height) // 2

            # Draw portrait background/border
            portrait_bg_rect = pygame.Rect(
                portrait_x - 4,
                portrait_y - 4,
                self.portrait_width + 8,
                self.portrait_height + 8,
            )
            pygame.draw.rect(screen, self.color_blue_light, portrait_bg_rect)
            pygame.draw.rect(screen, self.color_border, portrait_bg_rect, 2)

            # Draw portrait
            screen.blit(self.portrait, (portrait_x, portrait_y))

        # Calculate text area
        text_area_x = self.portrait_margin + self.portrait_width + self.text_margin + 4
        text_area_width = self.screen_width - text_area_x - self.text_margin
        text_area_y = content_y + self.text_margin
        text_area_height = content_height - (self.text_margin * 2)

        # Draw text
        max_text_width = text_area_width - 8
        wrapped_lines = self._wrap_text(self._displayed_text, max_text_width)

        line_height = self.font.get_height() + 3
        max_lines = text_area_height // line_height
        for i, line in enumerate(wrapped_lines):
            if i >= max_lines:
                break
            text_y = text_area_y + (i * line_height)
            text_surface = self.font.render(line, True, self.color_black)
            screen.blit(text_surface, (text_area_x, text_y))

        # Draw bottom blue border
        bottom_border_rect = pygame.Rect(
            0,
            int(self._current_y) + self.box_height - self.border_height,
            self.screen_width,
            self.border_height,
        )
        pygame.draw.rect(screen, self.color_blue_dark, bottom_border_rect)

        # Draw continue indicator if text is complete
        if self._char_index >= len(self._full_text):
            indicator_x = self.screen_width - 30
            indicator_y = int(self._current_y) + self.box_height - self.border_height - 25
            # Small bouncing arrow or dot
            pygame.draw.circle(screen, self.color_blue_dark, (indicator_x, indicator_y), 4)
