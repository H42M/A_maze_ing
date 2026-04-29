"""Maze cell module.

Provides a Cell class representing individual cells in the maze
with walls, textures, and rendering functionality.
"""

from render.RenderBloc import Bloc
from typing import Optional, Union
from Config.GameState import GameState
import pygame


class Cell:
    """Represents a single cell in the maze.

    A cell has four walls (north, south, east, west) and can render
    itself on a pygame surface. Supports textures for walls, entry,
    exit, and solution path indicators.

    Attributes:
        x (int): X coordinate of cell in maze grid.
        y (int): Y coordinate of cell in maze grid.
        pos (tuple[int, int]): Position tuple (x, y).
        _n (bool): Whether north wall exists.
        _s (bool): Whether south wall exists.
        _e (bool): Whether east wall exists.
        _w (bool): Whether west wall exists.
    """

    def __init__(self, x: int, y: int,
                 color: Union[tuple[int, int, int], pygame.Surface]) -> None:
        """Initialize a maze cell.

        Args:
            x (int): X coordinate in the maze grid.
            y (int): Y coordinate in the maze grid.
            color (Union[tuple[int, int, int], pygame.Surface]): Cell color
                as RGB tuple or pygame Surface for texture.
        """
        self._n = True
        self._s = True
        self._e = True
        self._w = True
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.__is42 = False

        self.__render_cell: list[Bloc] = []

        self.__color: Optional[tuple[int, int, int]] = None
        self.__wall_texture: Optional[pygame.Surface] = None
        self.__entry_texture: Optional[pygame.Surface] = None
        self.__exit_texture: Optional[pygame.Surface] = None
        self.__soluce_texture: Optional[pygame.Surface] = None
        if isinstance(color, pygame.Surface):
            self.__wall_texture = color
        else:
            self.__color = color

        self.__display_soluce: bool = False
        self.__soluce_loaded: bool = False
        self.__exit_loaded: bool = False

    def render(self, screen: pygame.Surface) -> None:
        """Render the cell and all its components on the screen.

        Args:
            screen (pygame.Surface): The display surface to render on.
        """
        self.get_render_cell()
        for elm in self.__render_cell:
            elm.render(screen)

    def get_render_cell(self):
        """Get the list of render blocks for this cell.

        Generates render blocks if not already created, and handles
        loading of exit and solution textures.

        Returns:
            list[Bloc]: List of Bloc objects to render.
        """
        if len(self.__render_cell) == 0:
            self.set_render_cell()

        if (self.__soluce_texture and not self.__soluce_loaded and
                self.__display_soluce):
            self.__set_render_item(self.__soluce_texture)
            print('Soluce displayed')
            self.__soluce_loaded = True
        if self.__exit_texture and not self.__exit_loaded:
            print('Exit displayed')
            self.__set_render_item(self.__exit_texture)
            self.__exit_loaded = True
            print("Exit loaded")

        return self.__render_cell

    def set_render_cell(self):
        """Generate and set all wall blocks for rendering.

        Creates individual block objects for each wall segment based on
        the cell's wall configuration and size settings.
        """
        self.reset_render()

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
        """Add a texture item to the render list.

        Args:
            item (pygame.Surface): The texture surface to render.
        """
        size = GameState.get_cell_size()

        xpos = self.x * size[0] + GameState.gap[0]
        ypos = self.y * size[1] + GameState.gap[1]

        xpos += (size[0]) // 2
        ypos += (size[1]) // 2
        self.__render_cell.append(
            Bloc((xpos, ypos), texture=item,
                 collision=False)
        )

    def set_entry_texture(self, entry_texture: pygame.Surface):
        """Set the texture for the entry point.

        Args:
            entry_texture (pygame.Surface): The entry texture surface.
        """
        self.__entry_texture = entry_texture
        self.reset_render()

    def set_exit_texture(self, entry_texture: pygame.Surface):
        """Set the texture for the exit point.

        Args:
            entry_texture (pygame.Surface): The exit texture surface.
        """
        self.__exit_texture = entry_texture
        self.reset_render()

    def set_soluce_texture(self, soluce_texture: pygame.Surface):
        """Set the texture for the solution path indicator.

        Args:
            soluce_texture (pygame.Surface): The solution texture surface.
        """
        self.__soluce_texture = soluce_texture
        self.reset_render()

    def reset_render(self):
        """Reset all render blocks and state flags.

        Clears cached render blocks and resets texture loading flags.
        """
        self.__render_cell = []
        self.__exit_loaded = False
        self.__soluce_loaded = False

    @property
    def n(self) -> bool:
        """Get whether north wall exists.

        Returns:
            bool: True if north wall exists, False otherwise.
        """
        return self._n

    @n.setter
    def n(self, value):
        """Set whether north wall exists.

        Args:
            value (bool): True to create north wall, False to remove it.
        """
        self._n = value

    @property
    def s(self) -> bool:
        """Get whether south wall exists.

        Returns:
            bool: True if south wall exists, False otherwise.
        """
        return self._s

    @s.setter
    def s(self, value):
        """Set whether south wall exists.

        Args:
            value (bool): True to create south wall, False to remove it.
        """
        self._s = value

    @property
    def e(self) -> bool:
        """Get whether east wall exists.

        Returns:
            bool: True if east wall exists, False otherwise.
        """
        return self._e

    @e.setter
    def e(self, value):
        """Set whether east wall exists.

        Args:
            value (bool): True to create east wall, False to remove it.
        """
        self._e = value

    @property
    def w(self) -> bool:
        """Get whether west wall exists.

        Returns:
            bool: True if west wall exists, False otherwise.
        """
        return self._w

    @w.setter
    def w(self, value):
        """Set whether west wall exists.

        Args:
            value (bool): True to create west wall, False to remove it.
        """
        self._w = value

    @property
    def is42(self) -> bool:
        """Get whether this cell is part of the 42 logo.

        Returns:
            bool: True if cell is part of the logo, False otherwise.
        """
        return self.__is42

    @is42.setter
    def is42(self, value):
        """Set whether this cell is part of the 42 logo.

        Args:
            value (bool): True to mark as part of logo, False otherwise.
        """
        self.__is42 = value

    @property
    def color(self):
        """Get the cell's color.

        Returns:
            tuple[int, int, int]: RGB color tuple or None if textured.
        """
        return self.__color

    @color.setter
    def color(self, value: tuple[int, int, int]):
        """Set the cell's color and reset rendering.

        Args:
            value (tuple[int, int, int]): RGB color tuple.
        """
        print(f"Setting color for cell ({self.x}, {self.y}): {value}")
        self.__color = value
        self.__render_cell = []

    @property
    def display_soluce(self) -> bool:
        """Get whether solution path should be displayed.

        Returns:
            bool: True if solution is displayed, False otherwise.
        """
        return self.__display_soluce

    @display_soluce.setter
    def display_soluce(self, value) -> None:
        """Set whether to display solution path and update rendering.

        Args:
            value (bool): True to show solution, False to hide it.
        """
        self.__display_soluce = value
        self.reset_render()

    @property
    def wall_texture(self):
        """Get the cell's wall texture.

        Returns:
            pygame.Surface: The wall texture surface or None.
        """
        return self.__wall_texture

    @wall_texture.setter
    def wall_texture(self, value):
        """Set the cell's wall texture and reset rendering.

        Args:
            value (pygame.Surface): The wall texture surface.
        """
        self.__wall_texture = value
        self.__render_cell = []
