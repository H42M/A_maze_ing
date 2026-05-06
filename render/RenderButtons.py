from render.RenderObj import RenderObj
import pygame
from typing import Optional, Union, Any
from collections.abc import Callable


class Button(RenderObj):
    """Render an interactive button."""

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
        """Initialize the button."""
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
        """Return a brighter RGB color."""
        r, g, b = color
        return (min(255, r + amount), min(255, g + amount),
                min(255, b + amount))

    def _darken(self, color: tuple[int, int, int], amount: int
                ) -> tuple[int, int, int]:
        """Return a darker RGB color."""
        r, g, b = color
        return (max(0, r - amount), max(0, g - amount), max(0, b - amount))

    def _apply_hover(self, color: tuple[int, int, int]
                     ) -> tuple[int, int, int]:
        """Apply the hover effect to a color."""
        return (self._brighten(color, self.HOVER_BRIGHTNESS)
                if self._is_hovered else color)

    def _get_border_color(self, base_color: tuple[int, int, int]
                          ) -> tuple[int, int, int]:
        """Return the button border color."""
        return self._darken(base_color, self.BORDER_DARKEN)

    def _draw_shadow(self, screen: pygame.Surface) -> None:
        """Draw the button shadow."""
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
        """Draw the button body."""
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
        """Draw centered text."""
        font = font or self._font
        text_surf = font.render(text, True, self._text_color)
        surface.blit(
            text_surf,
            text_surf.get_rect(center=(self._size[0] // 2,
                                       self._size[1] // 2)),
        )

    def _resolve_color(self) -> tuple[int, int, int]:
        """Return the current button color."""
        base = (self._hover_color if self._is_hovered and self._hover_color
                else self._color)
        if not base:
            base = (255, 0, 0)
        return self._apply_hover(base)

    def _blit_to_screen(self, screen: pygame.Surface) -> None:
        """Blit the button surface to the screen."""
        if self._surface:
            screen.blit(self._surface, (int(self._pos.x), int(self._pos.y)))

    # ------------------------------------------------------------------ #
    #  Rendu                                                               #
    # ------------------------------------------------------------------ #

    def render(self, screen: pygame.Surface) -> None:
        """Render the button."""
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
        """Return the button bounds."""
        return pygame.Rect(int(self._pos.x), int(self._pos.y), *self._size)

    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """Return whether the mouse position clicks the button."""
        return self._get_rect().collidepoint(mouse_pos)

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        """Update the hover state."""
        self._is_hovered = self._get_rect().collidepoint(mouse_pos)

    def execute(self) -> None:
        """Run the button callback."""
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
        """Set the button callback."""
        self._callback = callback

    def set_hover_color(self, color: tuple[int, int, int]) -> None:
        """Set the hover color."""
        self._hover_color = color

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value


# ------------------------------------------------------------------ #
#  Sous-classes                                                        #
# ------------------------------------------------------------------ #


class ToggleButton(Button):
    """Render a button with state-dependent color."""

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
        """Initialize the toggle button."""
        super().__init__(text, pos, size, callback=callback)
        self._callback_state = callback_state
        self._disable_color = disable_color or self.DEFAULT_DISABLE_COLOR
        self._enable_color = enable_color or self.DEFAULT_ENABLE_COLOR

    def _resolve_color(self) -> tuple[int, int, int]:
        base = (self._enable_color if self._callback_state()
                else self._disable_color)
        return self._apply_hover(base)


class SelectButton(Button):
    """Render a cyclic option selector."""

    def __init__(
        self,
        text: str,
        callback: Callable[[str], Any],
        options: list[str],
        pos: Optional[tuple[int, int]] = None,
        size: Optional[tuple[int, int]] = None,
    ) -> None:
        """Initialize the select button."""
        super().__init__(text, pos, size, color=(50, 100, 180),
                         callback=callback)
        self._options = options
        self.selected_opt: int = 0
        self._font_small = pygame.font.Font(None, 22)

    @property
    def selected_value(self) -> str:
        return self._options[self.selected_opt]

    def _resolve_color(self) -> tuple[int, int, int]:
        if not self._color:
            return self._apply_hover((255, 0, 0))
        return self._apply_hover(self._color)

    def render(self, screen: pygame.Surface) -> None:
        """Render the select button."""
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
        """Select the next option and run the callback."""
        if not self._callback:
            return
        if callable(self._callback):
            self.selected_opt = (self.selected_opt + 1) % len(self._options)
            self._callback(self.selected_value)
