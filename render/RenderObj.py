import pygame
from typing import Optional


class RenderObj:
    def __init__(self, pos: tuple[int, int],
                 size: tuple[int, int],
                 color: Optional[tuple[int, int, int]] = None,
                 collision: Optional[bool] = True
                 ) -> None:
        if color:
            self.__color = color
        else:
            self.__color = (255, 255, 0)

        self.__pos = pygame.Vector2(pos[0], pos[1])
        self.__size = size
        self.__collision = collision

        self.__surface = pygame.Surface(self.__size)
        self.__surface.fill(self.__color)

    def render(self, screen: pygame.Surface):
        self._surface.fill(self._color)
        pos_tuple = (int(self._pos.x), int(self._pos.y))
        screen.blit(self._surface, pos_tuple)

    @property
    def _color(self):
        return self.__color

    @_color.setter
    def _color(self, value: tuple[int, int, int]):
        self.__color = value

    @property
    def _pos(self):
        return self.__pos

    @_pos.setter
    def _pos(self, value):
        self.__pos = value

    @property
    def _size(self):
        return self.__size

    @_size.setter
    def _size(self, value):
        self.__size = value

    @property
    def _surface(self):
        return self.__surface

    @_surface.setter
    def _surface(self, value):
        self.__surface = value

    @property
    def collision(self):
        return self.__collision

    @collision.setter
    def collision(self, value):
        self.__collision = value
