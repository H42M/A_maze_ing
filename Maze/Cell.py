from render.RenderBloc import Bloc
from typing import Union
from Config.GameState import GameState
import pygame


class Cell:
    def __init__(self, x: int, y: int,
                 color: tuple[int, int, int]) -> None:
        self._n = True
        self._s = True
        self._e = True
        self._w = True
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)

        self.__nb_bloc = GameState.get_cell_nb_bloc()
        self.__cell_size = GameState.get_cell_size()
        self.__bloc_size = GameState.get_bloc_size()

        self.__render_cell: list[Bloc] = []
        self.__color: Union[str, tuple[int, int, int]] = color

    def render(self, screen: pygame.Surface) -> None:
        self.get_render_cell()
        for elm in self.__render_cell:
            elm.render(screen)

    def get_render_cell(self):
        if len(self.__render_cell) == 0:
            self.set_render_cell()
        return self.__render_cell

    def set_render_cell(self):
        cell_size = self.__cell_size

        xpos = (self.x * self.__cell_size[0]) + GameState.get_gap()[0]
        ypos = (self.y * self.__cell_size[1]) + + GameState.get_gap()[1]
        wall_bloc = []

        if self._n:
            for i in range(0, cell_size[0], GameState.bloc_size[0]):
                wall_bloc.append(Bloc((xpos + i, ypos),
                                      self.__color))
        if self._s:
            wall_y = ypos + cell_size[1]
            for i in range(0, cell_size[0], GameState.bloc_size[0]):
                wall_bloc.append(Bloc((xpos + i, wall_y),
                                      self.__color))
        if self._e:
            wall_x = xpos + cell_size[0]
            for i in range(0, cell_size[1], GameState.bloc_size[1]):
                wall_bloc.append(Bloc((wall_x, ypos + i),
                                      self.__color))
        if self._w:
            for i in range(0, cell_size[1], GameState.bloc_size[1]):
                wall_bloc.append(Bloc((xpos, ypos + i),
                                      self.__color))
        self.__render_cell = wall_bloc

    @property
    def n(self) -> bool:
        return self._n

    @n.setter
    def n(self, value):
        self._n = value

    @property
    def s(self) -> bool:
        return self._s

    @s.setter
    def s(self, value):
        self._s = value

    @property
    def e(self) -> bool:
        return self._e

    @e.setter
    def e(self, value):
        self._e = value

    @property
    def w(self) -> bool:
        return self._w

    @w.setter
    def w(self, value):
        self._w = value

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value: Union[tuple[int, int, int], str]):
        print(f"Setting color for cell ({self.x}, {self.y}): {value}")
        self.__color = value
        self.__render_cell = []
