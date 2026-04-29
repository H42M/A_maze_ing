"""Render text module.

Provides a RenderText class for rendering text on pygame surfaces
with customizable fonts and positioning.
"""

from render.RenderObj import RenderObj

import pygame
from typing import Optional


class RenderText(RenderObj):
    """Text rendering object.

    Renders text centered on a rectangular area with customizable font size
    and background color.

    Attributes:
        _RenderText__font_size (int): Font size in pixels.
        _RenderText__font (pygame.font.Font): Font object.
        _RenderText__text (str): Text to render.
    """

    def __init__(self,
                 pos: tuple[int, int],
                 size: tuple[int, int],
                 text: str,
                 bg_color: Optional[tuple[int, int, int]] = None,
                 font_size: Optional[int] = None
                 ) -> None:
        """Initialize a text render object.

        Args:
            pos (tuple[int, int]): Text position (x, y).
            size (tuple[int, int]): Bounding box size (width, height).
            text (str): The text to render.
            bg_color (Optional[tuple[int, int, int]]): Background color.
            font_size (Optional[int]): Font size in pixels. Defaults to 28.
        """
        super().__init__(pos, size, bg_color, collision=False)
        if not font_size:
            self.__font_size = 28
        else:
            self.__font_size = font_size
        self.__font = pygame.font.Font(None, self.__font_size)
        self.__text = text

    def render(self, screen: pygame.Surface) -> None:
        """Render the text centered on the screen.

        Args:
            screen (pygame.Surface): The display surface to render on.
        """
        text_surf = self.__font.render(self.__text, True, (0, 0, 0),
                                       self._color)
        text_rect = text_surf.get_rect(center=(self._pos[0] + self._size[0]
                                               // 2,
                                               self._pos[1] + self._size[1]
                                               // 2))
        screen.blit(text_surf, text_rect)
