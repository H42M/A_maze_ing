import pygame
from typing import Optional


class RenderObj:
    def __init__(self, pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 color: Optional[tuple[int, int, int]] = None,
                 collision: Optional[bool] = True
                 ) -> None:
        if color:
            self.__color = color
        else:
            self.__color = (255, 255, 0)

        self.__pos: Optional[pygame.Vector2] = None
        self.__size: Optional[tuple] = None
        self.__surface: Optional[pygame.Surface] = None

        if pos and size:
            self.__pos = pygame.Vector2(pos[0], pos[1])
            self.__size = size
            self.__surface = pygame.Surface(self.__size)
            self.__surface.fill(self.__color)

        self.__collision = collision

    def render(self, screen: pygame.Surface):
        if self.__surface and self.__pos:
            self.__surface.fill(self.__color)
            pos_tuple = (int(self.__pos.x), int(self.__pos.y))
            screen.blit(self.__surface, pos_tuple)

    @property
    def _color(self):
        return self.__color

    @_color.setter
    def _color(self, value: tuple[int, int, int]):
        self.__color = value

    @property
    def _pos(self) -> pygame.Vector2:
        if not self.__pos:
            return pygame.Vector2(0, 0)
        return self.__pos

    @_pos.setter
    def _pos(self, value: pygame.Vector2):
        self.__pos = value

    @property
    def _size(self) -> tuple[int, int]:
        if not self.__size:
            return (0, 0)
        return self.__size

    @_size.setter
    def _size(self, value: tuple[int, int]):
        self.__size = value
        self.__surface = pygame.Surface(self.__size)

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
