import pygame
from typing import Optional


class RenderObj:
    """Base renderable object."""

    def __init__(self, pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 color: Optional[tuple[int, int, int]] = None,
                 collision: Optional[bool] = True
                 ) -> None:
        """Initialize the render object."""
        self.__color = color

        self.__pos: Optional[pygame.Vector2] = None
        self.__size: Optional[tuple[int, int]] = None
        self.__surface: Optional[pygame.Surface] = None

        if pos and size:
            self.__pos = pygame.Vector2(pos[0], pos[1])
            self.__size = size
            self.__surface = pygame.Surface(self.__size)
            if color:
                self.__surface.fill(color)

        self.__collision = collision

    def render(self, screen: pygame.Surface) -> None:
        """Render the object."""
        if self.__surface and self.__pos:
            pos_tuple = (int(self.__pos.x), int(self.__pos.y))
            screen.blit(self.__surface, pos_tuple)
            if self.__color:
                self.__surface.fill(self.__color)

    @property
    def _color(self) -> Optional[tuple[int, int, int]]:
        return self.__color

    @_color.setter
    def _color(self, value: tuple[int, int, int]) -> None:
        self.__color = value

    @property
    def _pos(self) -> pygame.Vector2:
        if not self.__pos:
            return pygame.Vector2(0, 0)
        return self.__pos

    @_pos.setter
    def _pos(self, value: pygame.Vector2) -> None:
        self.__pos = value

    @property
    def _size(self) -> tuple[int, int]:
        if not self.__size:
            return (0, 0)
        return self.__size

    @_size.setter
    def _size(self, value: tuple[int, int]) -> None:
        self.__size = value
        self.__surface = pygame.Surface(self.__size)

    @property
    def _surface(self) -> Optional[pygame.Surface]:
        return self.__surface

    @_surface.setter
    def _surface(self, value: pygame.Surface) -> None:
        self.__surface = value

    @property
    def collision(self) -> Optional[bool]:
        return self.__collision

    @collision.setter
    def collision(self, value: bool) -> None:
        self.__collision = value