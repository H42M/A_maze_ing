"""Base render object module.

Provides the RenderObj base class for all renderable game objects
with position, size, color, and collision support.
"""

import pygame
from typing import Optional


class RenderObj:
    """Base class for renderable objects.

    Provides position, size, color, and collision management for
    rendering rectangles on the pygame display.

    Attributes:
        _RenderObj__pos (pygame.Vector2): Object position.
        _RenderObj__size (tuple): Object dimensions.
        _RenderObj__color (tuple): RGB color values.
        _RenderObj__surface (pygame.Surface): Rendered surface.
        _RenderObj__collision (bool): Whether object has collision.
    """
    def __init__(self, pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 color: Optional[tuple[int, int, int]] = None,
                 collision: Optional[bool] = True
                 ) -> None:
        """Initialize a render object.

        Args:
            pos (Optional[tuple[int, int]]): Position (x, y).
            size (Optional[tuple[int, int]]): Size (width, height).
            color (Optional[tuple[int, int, int]]): RGB color value.
            collision (Optional[bool]): Whether object has collision.
                Defaults to True.
        """

        self.__color = color

        self.__pos: Optional[pygame.Vector2] = None
        self.__size: Optional[tuple] = None
        self.__surface: Optional[pygame.Surface] = None

        if pos and size:
            self.__pos = pygame.Vector2(pos[0], pos[1])
            self.__size = size
            self.__surface = pygame.Surface(self.__size)
            if color:
                self.__surface.fill(color)

        self.__collision = collision

    def render(self, screen: pygame.Surface):
        """Render this object on the screen.

        Args:
            screen (pygame.Surface): The display surface to render on.
        """
        if self.__surface and self.__pos:
            pos_tuple = (int(self.__pos.x), int(self.__pos.y))
            screen.blit(self.__surface, pos_tuple)
            if self.__color:
                self.__surface.fill(self.__color)

    @property
    def _color(self):
        """Get the object's color.

        Returns:
            tuple[int, int, int]: RGB color tuple or None.
        """
        return self.__color

    @_color.setter
    def _color(self, value: tuple[int, int, int]):
        """Set the object's color.

        Args:
            value (tuple[int, int, int]): RGB color tuple.
        """
        self.__color = value

    @property
    def _pos(self) -> pygame.Vector2:
        """Get the object's position.

        Returns:
            pygame.Vector2: Position vector (x, y).
        """
        if not self.__pos:
            return pygame.Vector2(0, 0)
        return self.__pos

    @_pos.setter
    def _pos(self, value: pygame.Vector2):
        """Set the object's position.

        Args:
            value (pygame.Vector2): New position vector.
        """
        self.__pos = value

    @property
    def _size(self) -> tuple[int, int]:
        """Get the object's dimensions.

        Returns:
            tuple[int, int]: Size (width, height).
        """
        if not self.__size:
            return (0, 0)
        return self.__size

    @_size.setter
    def _size(self, value: tuple[int, int]):
        """Set the object's dimensions and recreate surface.

        Args:
            value (tuple[int, int]): New size (width, height).
        """
        self.__size = value
        self.__surface = pygame.Surface(self.__size)

    @property
    def _surface(self):
        """Get the object's pygame surface.

        Returns:
            pygame.Surface: The rendered surface or None.
        """
        return self.__surface

    @_surface.setter
    def _surface(self, value):
        """Set the object's pygame surface.

        Args:
            value (pygame.Surface): The new surface.
        """
        self.__surface = value

    @property
    def collision(self):
        """Get collision status.

        Returns:
            bool: True if object has collision, False otherwise.
        """
        return self.__collision

    @collision.setter
    def collision(self, value):
        """Set collision status.

        Args:
            value (bool): True to enable collision, False to disable.
        """
        self.__collision = value
