"""Button rendering module.

Provides Button, ToggleButton, and SelectButton classes for interactive
UI elements with hover effects, shadows, and rounded borders.
"""

from render.RenderObj import RenderObj
import pygame
from typing import Optional, Union, Any
from collections.abc import Callable


class Button(RenderObj):
    """Base button class with hover effects and shadow.

    Provides a base button with rounded corners, shadow effect, hover
    brightness change, and callback execution.

    Attributes:
        BORDER_RADIUS (int): Radius for rounded corners.
        BORDER_WIDTH (int): Width of button border.
        DEFAULT_COLOR (tuple): Default button color.
        SHADOW_COLOR (tuple): Color of drop shadow.
        HOVER_BRIGHTNESS (int): Brightness increase on hover.
        BORDER_DARKEN (int): Amount to darken border.
    """

    BORDER_RADIUS = 8
    BORDER_WIDTH = 2
    # DEFAULT_COLOR = (100, 150, 200)
    DEFAULT_COLOR = (255, 0, 0)

    SHADOW_COLOR = (40, 40, 40)
    HOVER_BRIGHTNESS = 40
    BORDER_DARKEN = 80

    def __init__(
        self,
        text: str,
        pos: Optional[tuple[int, int]] = None,
        size: Optional[tuple[int, int]] = None,
        color: Optional[tuple[int, int, int]] = None,
        callback: Optional[Union[Callable[..., Any],
                                 list[Callable[..., Any]]]] = None,
    ) -> None:
        """Initialize a button.

        Args:
            text (str): Button display text.
            pos (Optional[tuple[int, int]]): Button position (x, y).
            size (Optional[tuple[int, int]]): Button size (width, height).
            color (Optional[tuple[int, int, int]]): Button color as RGB tuple.
            callback (Optional[Union[Callable, list[Callable]]]): Function(s)
                to call when button is clicked.
        """
        super().__init__(pos, size, color or self.DEFAULT_COLOR)
        self._text = text
        self._callback = callback
        self._is_hovered = False
        self._hover_color: tuple[int, int, int] | None = None
        self._font = pygame.font.Font(None, 28)
        self._text_color = (255, 255, 255)

    # ------------------------------------------------------------------ #
    #  Helpers partagés                                                    #
    # ------------------------------------------------------------------ #

    def _brighten(self, color: tuple[int, int, int], amount: int
                  ) -> tuple[int, int, int]:
        """Brighten an RGB color by a given amount.

        Args:
            color (tuple[int, int, int]): RGB color to brighten.
            amount (int): Amount to brighten each channel.

        Returns:
            tuple[int, int, int]: Brightened RGB color (capped at 255).
        """
        r, g, b = color
        return (min(255, r + amount), min(255, g + amount),
                min(255, b + amount))

    def _darken(self, color: tuple[int, int, int], amount: int
                ) -> tuple[int, int, int]:
        """Darken an RGB color by a given amount.

        Args:
            color (tuple[int, int, int]): RGB color to darken.
            amount (int): Amount to darken each channel.

        Returns:
            tuple[int, int, int]: Darkened RGB color (capped at 0).
        """
        r, g, b = color
        return (max(0, r - amount), max(0, g - amount), max(0, b - amount))

    def _apply_hover(self, color: tuple[int, int, int]
                     ) -> tuple[int, int, int]:
        """Apply hover brightness effect to a color.

        Args:
            color (tuple[int, int, int]): Base color.

        Returns:
            tuple[int, int, int]: Brightened color if hovering, else original.
        """
        return (self._brighten(color, self.HOVER_BRIGHTNESS)
                if self._is_hovered else color)

    def _get_border_color(self, base_color: tuple[int, int, int]
                          ) -> tuple[int, int, int]:
        """Get a darker color for button border.

        Args:
            base_color (tuple[int, int, int]): Base button color.

        Returns:
            tuple[int, int, int]: Darkened border color.
        """
        return self._darken(base_color, self.BORDER_DARKEN)

    def _draw_shadow(self, screen: pygame.Surface) -> None:
        """Draw drop shadow beneath the button.

        Args:
            screen (pygame.Surface): The display surface to draw on.
        """
        offset = 4 if self._is_hovered else 2
        shadow = pygame.Surface(self._size)
        shadow.set_colorkey((0, 0, 0))
        pygame.draw.rect(
            shadow,
            self.SHADOW_COLOR,
            (0, 0, *self._size),
            border_radius=self.BORDER_RADIUS,
        )
        screen.blit(shadow, (int(self._pos.x) + offset,
                             int(self._pos.y) + offset))

    def _draw_rounded_rect(
        self,
        surface: pygame.Surface,
        fill_color: tuple[int, int, int],
        border_color: tuple[int, int, int],
    ) -> None:
        """Draw a rounded rectangle with fill and border.

        Args:
            surface (pygame.Surface): Surface to draw on.
            fill_color (tuple[int, int, int]): Fill color RGB.
            border_color (tuple[int, int, int]): Border color RGB.
        """
        rect = (0, 0, *self._size)

        pygame.draw.rect(surface, fill_color, rect,
                         border_radius=self.BORDER_RADIUS)
        pygame.draw.rect(
            surface, border_color, rect, self.BORDER_WIDTH,
            border_radius=self.BORDER_RADIUS
        )

    def _blit_centered_text(
        self,
        surface: pygame.Surface,
        text: str,
        font: pygame.font.Font | None = None,
    ) -> None:
        """Draw centered text on a surface.

        Args:
            surface (pygame.Surface): Surface to draw text on.
            text (str): Text to render.
            font (Optional[pygame.font.Font]): Font to use. If None,
            uses default.
        """
        font = font or self._font
        text_surf = font.render(text, True, self._text_color)
        surface.blit(
            text_surf,
            text_surf.get_rect(center=(self._size[0] // 2,
                                       self._size[1] // 2)),
        )

    def _resolve_color(self) -> tuple[int, int, int]:
        """Get the color to use for current frame.

        Can be overridden by subclasses for different state logic.

        Returns:
            tuple[int, int, int]: The color to render with.
        """
        base = (self._hover_color if self._is_hovered and self._hover_color
                else self._color)
        if not base:
            base = (255, 0, 0)
        return self._apply_hover(base)

    def _blit_to_screen(self, screen: pygame.Surface) -> None:
        """Copy internal surface to screen at button position.

        Args:
            screen (pygame.Surface): The display surface to blit to.
        """
        if self._surface:
            screen.blit(self._surface, (int(self._pos.x), int(self._pos.y)))

    # ------------------------------------------------------------------ #
    #  Rendu                                                               #
    # ------------------------------------------------------------------ #

    def render(self, screen: pygame.Surface) -> None:
        """Render the current buttons's state.

        Args:
            screen (pygame.Surface): Render Screen
        """
        color = self._resolve_color()
        if self._surface:
            self._draw_shadow(screen)
            self._draw_rounded_rect(self._surface, color,
                                    self._get_border_color(color))
            self._blit_centered_text(self._surface, self._text)
            self._blit_to_screen(screen)

    # ------------------------------------------------------------------ #
    #  Interactions                                                        #
    # ------------------------------------------------------------------ #

    def _get_rect(self) -> pygame.Rect:
        """Get the button's rectangular bounds.

        Returns:
            pygame.Rect: Rectangle representing button position and size.
        """
        return pygame.Rect(int(self._pos.x), int(self._pos.y), *self._size)

    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """Check if mouse position is within button bounds.

        Args:
            mouse_pos (tuple[int, int]): Mouse position (x, y).

        Returns:
            bool: True if position is within button, False otherwise.
        """
        return self._get_rect().collidepoint(mouse_pos)

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        """Update hover state based on mouse position.

        Args:
            mouse_pos (tuple[int, int]): Current mouse position (x, y).
        """
        self._is_hovered = self._get_rect().collidepoint(mouse_pos)

    def execute(self) -> None:
        """Execute the button's callback function(s).

        Calls all registered callbacks for this button.
        """
        if not self._callback:
            return
        callbacks = (self._callback if isinstance(self._callback, list)
                     else [self._callback])
        for cb in callbacks:
            cb()

    # ------------------------------------------------------------------ #
    #  Setters                                                             #
    # ------------------------------------------------------------------ #

    def set_callback(self, callback: Callable[..., Any]) -> None:
        """Set or replace the button's callback function.

        Args:
            callback (Callable): Function to call when clicked.
        """
        self._callback = callback

    def set_hover_color(self, color: tuple[int, int, int]) -> None:
        """Set custom hover color.

        Args:
            color (tuple[int, int, int]): Hover color as RGB tuple.
        """
        self._hover_color = color

    @property
    def text(self) -> str:
        """Get the current button text.

        Return:
            str: current button text.
        """
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """Set the current button text.

        Args:
            value (str): current button text.
        """
        self._text = value


# ------------------------------------------------------------------ #
#  Sous-classes                                                        #
# ------------------------------------------------------------------ #


"""Toggle button subclass.

A button that changes color based on an external boolean state.
"""


class ToggleButton(Button):
    """Button with state-dependent color.

    Displays different colors based on a callback that returns a boolean
    state. Red when disabled, green when enabled.

    Attributes:
        DEFAULT_DISABLE_COLOR (tuple): Color when state is False.
        DEFAULT_ENABLE_COLOR (tuple): Color when state is True.
    """

    DEFAULT_DISABLE_COLOR = (200, 50, 50)
    DEFAULT_ENABLE_COLOR = (50, 180, 50)

    def __init__(
        self,
        text: str,
        callback: Callable[..., Any],
        callback_state: Callable[[], bool],
        disable_color: tuple[int, int, int] | None = None,
        enable_color: tuple[int, int, int] | None = None,
        pos: Optional[tuple[int, int]] = None,
        size: Optional[tuple[int, int]] = None,
    ) -> None:
        """Initialize a toggle button.

        Args:
            text (str): Button text.
            callback (Callable): Function to call when clicked.
            callback_state (Callable[[], bool]): Function returning state.
            disable_color (Optional[tuple]): Color when state is False.
            enable_color (Optional[tuple]): Color when state is True.
            pos (Optional[tuple[int, int]]): Button position.
            size (Optional[tuple[int, int]]): Button size.
        """
        super().__init__(text, pos, size, callback=callback)
        self._callback_state = callback_state
        self._disable_color = disable_color or self.DEFAULT_DISABLE_COLOR
        self._enable_color = enable_color or self.DEFAULT_ENABLE_COLOR

    def _resolve_color(self) -> tuple[int, int, int]:
        base = (self._enable_color if self._callback_state()
                else self._disable_color)
        return self._apply_hover(base)


"""Select button subclass.

A cyclic button that iterates through a list of options.
"""


class SelectButton(Button):
    """Cyclic option selector button.

    Cycles through a list of options on each click. Displays the button
    title at the top and selected option at the bottom.

    Attributes:
        _options (list[str]): List of available options.
        selected_opt (int): Index of currently selected option.
    """

    def __init__(
        self,
        text: str,
        callback: Callable[[str], Any],
        options: list[str],
        pos: Optional[tuple[int, int]] = None,
        size: Optional[tuple[int, int]] = None,
    ) -> None:
        """Initialize a select button.

        Args:
            text (str): Button title text.
            callback (Callable[[str], Any]): Function called with
            selected value.

            options (list[str]): List of options to cycle through.
            pos (Optional[tuple[int, int]]): Button position.
            size (Optional[tuple[int, int]]): Button size.
        """
        super().__init__(text, pos, size, color=(50, 100, 180),
                         callback=callback)
        self._options = options
        self.selected_opt: int = 0
        self._font_small = pygame.font.Font(None, 22)

    @property
    def selected_value(self) -> str:
        """Get the currently selected option.

        Returns:
            str: The currently selected option string.
        """
        return self._options[self.selected_opt]

    def _resolve_color(self) -> tuple[int, int, int]:
        if not self._color:
            return self._apply_hover((255, 0, 0))
        return self._apply_hover(self._color)

    def render(self, screen: pygame.Surface) -> None:
        """Render the current buttons's state.

        Args:
            screen (pygame.Surface): Render Screen
        """
        if not self._surface:
            return
        color = self._resolve_color()
        self._draw_shadow(screen)
        self._draw_rounded_rect(self._surface, color,
                                self._get_border_color(color))

        # Titre en haut (petite police)
        title_surf = self._font_small.render(self._text, True,
                                             self._text_color)
        self._surface.blit(title_surf,
                           title_surf.get_rect(midtop=(self._size[0] // 2, 5)))

        # Option sélectionnée en bas (police normale)
        option_surf = self._font.render(self.selected_value, True,
                                        self._text_color)
        self._surface.blit(
            option_surf,
            option_surf.get_rect(midbottom=(self._size[0] // 2,
                                            self._size[1] - 5)),
        )

        self._blit_to_screen(screen)

    def execute(self) -> None:
        """Cycle to next option and call callback with new selection.

        Moves to the next option in the list and calls the callback with
        the newly selected option string.
        """
        if not self._callback:
            return
        if callable(self._callback):
            self.selected_opt = (self.selected_opt + 1) % len(self._options)
            self._callback(self.selected_value)
