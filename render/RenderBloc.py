"""Render block module.

Provides a Bloc class that represents a renderable rectangular block
with optional texture support.
"""

from render.RenderObj import RenderObj
from typing import Optional
from Config.GameState import GameState
import pygame


class Bloc(RenderObj):
    """A renderable block with optional texture.

    Extends RenderObj to provide a block that can be rendered with
    either a solid color or a texture image.

    Attributes:
        image (pygame.Surface): The rendered block surface.
    """

    def __init__(self, pos: tuple[int, int],
                 color: Optional[tuple[int, int, int]] = None,
                 texture: Optional[pygame.Surface] = None,
                 collision: Optional[bool] = True
                 ):
        """Initialize a block.

        Args:
            pos (tuple[int, int]): Block position (x, y).
            color (Optional[tuple[int, int, int]]): RGB color if no texture.
            texture (Optional[pygame.Surface]): Texture surface to render.
            collision (Optional[bool]): Whether block has collision.
                Defaults to True.
        """
        super().__init__(pos=pos, size=GameState.bloc_size,
                         collision=collision)
        self.__texture = texture
        self.__color = color

    def render(self, screen):
        """Render the block on the screen.

        Renders the block with texture if available, otherwise with color.

        Args:
            screen (pygame.Surface): The display surface to render on.
        """
        if self.__texture:
            pos_tuple = (int(self._pos.x), int(self._pos.y))
            self.__texture = pygame.transform.scale(self.__texture, self._size)
            screen.blit(self.__texture, pos_tuple)
        else:
            super().render(screen)
