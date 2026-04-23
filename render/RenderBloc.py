from render.RenderObj import RenderObj
from typing import Optional
from Config.GameState import GameState
import pygame


class Bloc(RenderObj):

    image: pygame.Surface

    def __init__(self, pos: tuple[int, int],
                 color: Optional[tuple[int, int, int]] = None,
                 texture: Optional[pygame.Surface] = None,
                 collision: Optional[bool] = True
                 ):
        super().__init__(pos=pos, size=GameState.bloc_size,
                         collision=collision)
        self.__texture = texture
        self.__get_color(color)

    def render(self, screen):
        if self.__texture:
            pos_tuple = (int(self._pos.x), int(self._pos.y))
            self.__texture = pygame.transform.scale(self.__texture, self._size)
            screen.blit(self.__texture, pos_tuple)
        elif self.__is_image:
            pos_tuple = (int(self._pos.x), int(self._pos.y))
            screen.blit(self._surface, pos_tuple)
        else:
            super().render(screen)

    def __get_color(self, color):
        from random import randint

        # Sinon, traiter comme couleur
        self.__is_image = False
        if color == 'random':
            self._color = (randint(0, 255), randint(0, 255), randint(0, 255))
            self._surface.fill(self._color)
        elif isinstance(color, tuple):
            self._color = color
            self._surface.fill(self._color)
        else:
            self._color = (255, 255, 0)
            self._surface.fill(self._color)
