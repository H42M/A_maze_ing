from render.RenderObj import RenderObj

import pygame
from typing import Optional


class RenderText(RenderObj):
    """Render text inside a rectangle."""

    def __init__(self,
                 pos: tuple[int, int],
                 size: tuple[int, int],
                 text: str,
                 bg_color: Optional[tuple[int, int, int]] = None,
                 font_size: Optional[int] = None
                 ) -> None:
        """Initialize the text object."""
        super().__init__(pos, size, bg_color, collision=False)
        if not font_size:
            self.__font_size = 28
        else:
            self.__font_size = font_size
        self.__font = pygame.font.Font(None, self.__font_size)
        self.__text = text

    def render(self, screen: pygame.Surface) -> None:
        """Render the text."""
        text_surf = self.__font.render(self.__text, True, (0, 0, 0),
                                       self._color)
        text_rect = text_surf.get_rect(center=(self._pos[0] + self._size[0]
                                               // 2,
                                               self._pos[1] + self._size[1]
                                               // 2))
        screen.blit(text_surf, text_rect)