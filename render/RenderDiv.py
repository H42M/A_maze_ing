"""Render container modules.

Provides RenderDiv and RenderWindow classes for organizing renderable
objects in horizontal and vertical layouts.
"""

import pygame

from render.RenderObj import RenderObj
from typing import Optional, Union


class RenderDiv(RenderObj):
    """Horizontal container for render objects.

    Organizes child render objects in a horizontal layout with optional
    spacing and background color.

    Attributes:
        _content (list[RenderObj]): List of contained render objects.
        _gap (Optional[int]): Spacing between contained objects.
    """
    def __init__(self, pos: tuple[int, int],
                 size: tuple[int, int],
                 bg_color: Optional[tuple[int, int, int]] = None,
                 gap: Optional[int] = None
                 ) -> None:
        """Initialize a render division container.

        Args:
            pos (tuple[int, int]): Container position (x, y).
            size (tuple[int, int]): Container size (width, height).
            bg_color (Optional[tuple[int, int, int]]): Background color.
            gap (Optional[int]): Space between child objects.
        """
        super().__init__(pos, size, bg_color, collision=False)
        self._content: list[RenderObj] = []
        self._gap = gap

    def add(self, obj: Union[RenderObj, list[RenderObj]]) -> None:
        if isinstance(obj, list):
            self._content.extend(obj)
        else:
            self._content.append(obj)

    def render(self, screen: pygame.Surface):
        total_width = self._size[0]
        if self._gap:
            nb_gap = len(self._content) + 1
            total_gap = nb_gap * self._gap
            total_width -= total_gap
        space = total_width // len(self._content)

        for i, obj in enumerate(self._content):
            gap = 0
            if self._gap:
                gap = self._gap
            obj._pos = pygame.Vector2(self._pos.x + (gap * (i + 1)) +
                                      (space * i), self._pos.y)
            obj._size = (space, self._size[1])
            obj.render(screen)


"""Vertical window container.

A specialized render division that organizes objects vertically.
"""


class RenderWindow(RenderDiv):
    """Vertical container for render divisions.

    Organizes RenderDiv objects in a vertical layout with optional
    spacing and background color.
    """
    def __init__(self, pos: tuple[int, int],
                 size: tuple[int, int],
                 bg_color: Optional[tuple[int, int, int]] = None,
                 gap: Optional[int] = None) -> None:
        """Initialize a render window container.

        Args:
            pos (tuple[int, int]): Window position (x, y).
            size (tuple[int, int]): Window size (width, height).
            bg_color (Optional[tuple[int, int, int]]): Background color.
            gap (Optional[int]): Space between contained divisions.
        """
        super().__init__(pos, size, bg_color, gap)

    def add(self, obj: Union[RenderObj, list[RenderObj]]) -> None:
        if isinstance(obj, list):
            for o in obj:
                if isinstance(o, RenderDiv):
                    self._content.append(o)
                else:
                    print("Render window add incompatible obj")
        if isinstance(obj, RenderDiv):
            self._content.append(obj)
        else:
            print("Render window add incompatible obj")

    def render(self, screen: pygame.Surface):
        total_height = self._size[1]
        if self._gap:
            nb_gap = (len(self._content)) + 1
            total_gap = nb_gap * self._gap
            total_height -= total_gap
        space = total_height // len(self._content)

        print(f"Total height: {self._size[1]}")
        for i, div in enumerate(self._content):
            gap = 0
            if self._gap:
                gap = self._gap
            if isinstance(div, RenderDiv):
                pos_y = self._pos.y + (gap * (i + 1)) + (space * i)
                div._pos = pygame.Vector2(
                    self._pos.x,
                    pos_y
                )
                print(f"elm {i}: posy = {pos_y}")
                div._size = (self._size[0], space)
                div.render(screen)
