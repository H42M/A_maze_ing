import pygame

from render.RenderObj import RenderObj
from typing import Optional, Union


class RenderDiv(RenderObj):
    def __init__(self, pos: tuple[int, int],
                 size: tuple[int, int],
                 bg_color: Optional[tuple[int, int, int]] = None,
                 gap: Optional[int] = None
                 ) -> None:
        super().__init__(pos, size, bg_color, collision=False)
        self.__content: list[RenderObj] = []
        self.__gap = gap

    def add(self, obj: Union[RenderObj, list[RenderObj]]) -> None:
        if isinstance(obj, list):
            self.__content.extend(obj)
        else:
            self.__content.append(obj)

    def render(self, screen: pygame.Surface):
        total_width = self._size[0]
        if self.__gap:
            nb_gap = len(self.__content) + 1
            total_gap = nb_gap * self.__gap
            total_width -= total_gap
        space = total_width // len(self.__content)

        for i, obj in enumerate(self.__content):
            gap = 0
            if self.__gap: 
                gap = self.__gap
            obj._pos = pygame.Vector2(self._pos.x + (gap * (i + 1)) +
                                      (space * i), self._pos.y)
            obj._size = (space, self._size[1])
            obj.render(screen)
