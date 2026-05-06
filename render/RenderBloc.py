from render.RenderObj import RenderObj
from typing import Optional
from Config.GameState import GameState
import pygame


class Bloc(RenderObj):
    """Render a block with an optional texture."""

    def __init__(self, pos: tuple[int, int],
                 color: Optional[tuple[int, int, int]] = None,
                 texture: Optional[pygame.Surface] = None,
                 collision: Optional[bool] = True
                 ):
        """Initialize the block."""
        super().__init__(pos=pos, size=GameState.bloc_size,
                         collision=collision)
        self.__texture = texture
        self.__color = color

    def render(self, screen: pygame.Surface) -> None:
        """Render the block."""
        if self.__texture:
            pos_tuple = (int(self._pos.x), int(self._pos.y))
            self.__texture = pygame.transform.scale(self.__texture, self._size)
            screen.blit(self.__texture, pos_tuple)
        else:
            super().render(screen)
