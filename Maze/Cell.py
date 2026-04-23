from render.RenderBloc import Bloc
from typing import Optional
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
        self.__is42 = False

        self.__render_cell: list[Bloc] = []
        self.__color: tuple[int, int, int] = color
        self.__wall_texture: Optional[pygame.Surface] = None

        self.__soluce_block: bool = False
        self.__soluce_loaded: bool = False
        self.__exit_loaded: bool = False

    def render(self, screen: pygame.Surface,
               render_exit: bool = False, render_soluce: bool = False) -> None:
        self.get_render_cell(render_exit, render_soluce)
        for elm in self.__render_cell:
            elm.render(screen)

    def get_render_cell(self, render_exit: bool = False,
                        render_soluce: bool = False):
        if len(self.__render_cell) == 0:
            self.set_render_cell()

        if render_soluce and not self.__soluce_loaded:
            self.__set_render_item(GameState.soluce_texture)
            self.__soluce_loaded = True
        if render_exit and not self.__exit_loaded:
            self.__set_render_item(GameState.exit_texture)
            self.__exit_loaded = True
            print("Exit loaded")

        return self.__render_cell

    def set_render_cell(self):
        self.__render_cell = []
        self.__exit_loaded = False
        self.__soluce_loaded = False

        size = GameState.get_cell_size()

        xpos = (self.x * size[0]) + GameState.get_gap()[0]
        ypos = (self.y * size[1]) + + GameState.get_gap()[1]
        wall_bloc = []

        # Render Walls
        if self._n:
            for i in range(0, size[0], GameState.bloc_size[0]):
                wall_bloc.append(Bloc((xpos + i, ypos),
                                      self.__color, self.__wall_texture))
        if self._s:
            wall_y = ypos + size[1]
            for i in range(0, size[0], GameState.bloc_size[0]):
                wall_bloc.append(Bloc((xpos + i, wall_y),
                                      self.__color, self.__wall_texture))
        if self._e:
            wall_x = xpos + size[0]
            for i in range(0, size[1], GameState.bloc_size[1]):
                wall_bloc.append(Bloc((wall_x, ypos + i),
                                      self.__color, self.__wall_texture))
        if self._w:
            for i in range(0, size[1], GameState.bloc_size[1]):
                wall_bloc.append(Bloc((xpos, ypos + i),
                                      self.__color, self.__wall_texture))
        self.__render_cell = wall_bloc

    def __set_render_item(self, item: pygame.Surface):
        size = GameState.get_cell_size()

        xpos = self.x * size[0] + GameState.gap[0]
        ypos = self.y * size[1] + GameState.gap[1]

        xpos += (size[0]) // 2
        ypos += (size[1]) // 2
        self.__render_cell.append(
            Bloc((xpos, ypos), texture=item,
                 collision=False)
        )
        print(f"coin set at {xpos}, {ypos}")

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
    def is42(self) -> bool:
        return self.__is42

    @is42.setter
    def is42(self, value):
        self.__is42 = value

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value: tuple[int, int, int]):
        print(f"Setting color for cell ({self.x}, {self.y}): {value}")
        self.__color = value
        self.__render_cell = []

    @property
    def soluce_block(self) -> bool:
        return self.__soluce_block

    @soluce_block.setter
    def soluce_block(self, value):
        self.__soluce_block = value
        if not self.soluce_block:
            self.__render_cell = []

    @property
    def wall_texture(self):
        return self.__wall_texture

    @wall_texture.setter
    def wall_texture(self, value):
        self.__wall_texture = value
